$ErrorActionPreference = "Stop"

$Profile = "quantmind"
$Region = "us-east-2"

$Cluster = "quantmind-cluster"
$Service = "quantmind-service"

$VpcId = "vpc-02c35578872f7b2a0"

$PublicSubnetA = "subnet-039e1b0dd850459f0"
$PublicSubnetB = "subnet-0d66b54babaec0c80"

# NAT Gateway is created in this public subnet.
$NatSubnetId = "subnet-0d66b54babaec0c80"

$PrivateRouteTableId = "rtb-0700c15e6833f3118"

$AlbName = "quantmind-alb"
$AlbSecurityGroup = "sg-0a9ebf02107683934"

$TargetGroupName = "quantmind-tg"

function Check-AwsExit {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) {
        throw "AWS CLI failed during: $Step"
    }
}

Write-Host ""
Write-Host "[1/7] Checking NAT Gateway..."

$currentNatId = aws ec2 describe-route-tables `
    --route-table-ids $PrivateRouteTableId `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "RouteTables[0].Routes[?DestinationCidrBlock=='0.0.0.0/0'].NatGatewayId | [0]" `
    --output text
Check-AwsExit "reading private route table"

$natUsable = $false

if ($currentNatId -and $currentNatId -ne "None") {
    $currentNatState = aws ec2 describe-nat-gateways `
        --nat-gateway-ids $currentNatId `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --query "NatGateways[0].State" `
        --output text 2>$null

    if ($LASTEXITCODE -eq 0 -and $currentNatState -eq "available") {
        $natUsable = $true
        $newNatId = $currentNatId
        Write-Host "Existing NAT Gateway is available: $newNatId"
    }
}

if (-not $natUsable) {
    Write-Host "Allocating a new Elastic IP..."
    $allocationId = aws ec2 allocate-address `
        --domain vpc `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --query "AllocationId" `
        --output text
    Check-AwsExit "Elastic IP allocation"

    Write-Host "Creating NAT Gateway..."
    $newNatId = aws ec2 create-nat-gateway `
        --subnet-id $NatSubnetId `
        --allocation-id $allocationId `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --query "NatGateway.NatGatewayId" `
        --output text
    Check-AwsExit "NAT Gateway creation"

    Write-Host "Waiting for NAT Gateway $newNatId to become available..."
    aws ec2 wait nat-gateway-available `
        --nat-gateway-ids $newNatId `
        --profile $Profile `
        --region $Region
    Check-AwsExit "waiting for NAT Gateway"

    Write-Host ""
    Write-Host "[2/7] Restoring private default route..."

    $routeCount = aws ec2 describe-route-tables `
        --route-table-ids $PrivateRouteTableId `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --query "length(RouteTables[0].Routes[?DestinationCidrBlock=='0.0.0.0/0'])" `
        --output text
    Check-AwsExit "checking default route"

    if ([int]$routeCount -gt 0) {
        aws ec2 replace-route `
            --route-table-id $PrivateRouteTableId `
            --destination-cidr-block "0.0.0.0/0" `
            --nat-gateway-id $newNatId `
            --profile $Profile `
            --region $Region
        Check-AwsExit "replacing private default route"
    }
    else {
        aws ec2 create-route `
            --route-table-id $PrivateRouteTableId `
            --destination-cidr-block "0.0.0.0/0" `
            --nat-gateway-id $newNatId `
            --profile $Profile `
            --region $Region | Out-Null
        Check-AwsExit "creating private default route"
    }

    Write-Host "Private route now points to $newNatId"
}
else {
    Write-Host ""
    Write-Host "[2/7] Private NAT route already usable."
}

Write-Host ""
Write-Host "[3/7] Checking Application Load Balancer..."

$albArn = aws elbv2 describe-load-balancers `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "LoadBalancers[?LoadBalancerName=='$AlbName'].LoadBalancerArn | [0]" `
    --output text

Check-AwsExit "ALB discovery"

$albExists = ($albArn -and $albArn -ne "None")
if (-not $albExists) {
    Write-Host "Creating ALB $AlbName..."

    $albJson = aws elbv2 create-load-balancer `
        --name $AlbName `
        --subnets $PublicSubnetA $PublicSubnetB `
        --security-groups $AlbSecurityGroup `
        --scheme internet-facing `
        --type application `
        --ip-address-type ipv4 `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --output json
    Check-AwsExit "ALB creation"

    $albObj = $albJson | ConvertFrom-Json
    $albArn = $albObj.LoadBalancers[0].LoadBalancerArn
    $albDns = $albObj.LoadBalancers[0].DNSName

    Write-Host "Waiting for ALB to become available..."
    aws elbv2 wait load-balancer-available `
        --load-balancer-arns $albArn `
        --profile $Profile `
        --region $Region
    Check-AwsExit "waiting for ALB"
}
else {
    Write-Host "ALB already exists."
    $albDns = aws elbv2 describe-load-balancers `
        --load-balancer-arns $albArn `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --query "LoadBalancers[0].DNSName" `
        --output text
    Check-AwsExit "reading ALB DNS name"
}

Write-Host ""
Write-Host "[4/7] Checking target group and listener..."

$targetGroupArn = aws elbv2 describe-target-groups `
    --names $TargetGroupName `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "TargetGroups[0].TargetGroupArn" `
    --output text
Check-AwsExit "target group discovery"

$listenerCount = aws elbv2 describe-listeners `
    --load-balancer-arn $albArn `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "length(Listeners)" `
    --output text
Check-AwsExit "listener discovery"

if ([int]$listenerCount -eq 0) {
    Write-Host "Creating HTTP listener on port 80..."
    aws elbv2 create-listener `
        --load-balancer-arn $albArn `
        --protocol HTTP `
        --port 80 `
        --default-actions "Type=forward,TargetGroupArn=$targetGroupArn" `
        --profile $Profile `
        --region $Region `
        --no-cli-pager | Out-Null
    Check-AwsExit "listener creation"
}
else {
    Write-Host "Listener already exists."
}

Write-Host ""
Write-Host "[5/7] Starting ECS service..."

aws ecs update-service `
    --cluster $Cluster `
    --service $Service `
    --desired-count 1 `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "service.{Desired:desiredCount,Running:runningCount,Pending:pendingCount}" `
    --output table
Check-AwsExit "ECS scale up"

Write-Host ""
Write-Host "[6/7] Waiting for ECS service to stabilize..."

aws ecs wait services-stable `
    --cluster $Cluster `
    --services $Service `
    --profile $Profile `
    --region $Region
Check-AwsExit "waiting for ECS service"

Write-Host ""
Write-Host "[7/7] Checking target health..."

aws elbv2 describe-target-health `
    --target-group-arn $targetGroupArn `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "TargetHealthDescriptions[].{Target:Target.Id,Port:Target.Port,State:TargetHealth.State,Reason:TargetHealth.Reason}" `
    --output table
Check-AwsExit "target health check"

Write-Host ""
Write-Host "============================================================"
Write-Host "QuantMind is awake."
Write-Host "ALB DNS: $albDns"
Write-Host "Health URL: http://$albDns/health"
Write-Host "Swagger URL: http://$albDns/docs"
Write-Host "============================================================"
