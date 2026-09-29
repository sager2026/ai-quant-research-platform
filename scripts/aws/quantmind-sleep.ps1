param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$Profile = "quantmind"
$Region = "us-east-2"

$Cluster = "quantmind-cluster"
$Service = "quantmind-service"

$AlbName = "quantmind-alb"
$PrivateRouteTableId = "rtb-0700c15e6833f3118"

function Check-AwsExit {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) {
        throw "AWS CLI failed during: $Step"
    }
}

if (-not $Force) {
    $answer = Read-Host "This will scale ECS to 0 and DELETE the QuantMind ALB + active NAT Gateway/EIP. Type SLEEP to continue"
    if ($answer -ne "SLEEP") {
        Write-Host "Cancelled."
        exit 0
    }
}

Write-Host ""
Write-Host "[1/5] Scaling ECS service to zero..."
aws ecs update-service `
    --cluster $Cluster `
    --service $Service `
    --desired-count 0 `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "service.{Desired:desiredCount,Running:runningCount,Pending:pendingCount}" `
    --output table
Check-AwsExit "ECS scale down"

aws ecs wait services-stable `
    --cluster $Cluster `
    --services $Service `
    --profile $Profile `
    --region $Region
Check-AwsExit "waiting for ECS service to stabilize"

Write-Host ""
Write-Host "[2/5] Discovering and deleting ALB..."
$albArn = aws elbv2 describe-load-balancers `
    --names $AlbName `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "LoadBalancers[0].LoadBalancerArn" `
    --output text 2>$null

if ($LASTEXITCODE -eq 0 -and $albArn -and $albArn -ne "None") {
    aws elbv2 delete-load-balancer `
        --load-balancer-arn $albArn `
        --profile $Profile `
        --region $Region `
        --no-cli-pager
    Check-AwsExit "ALB deletion"

    aws elbv2 wait load-balancers-deleted `
        --load-balancer-arns $albArn `
        --profile $Profile `
        --region $Region
    Check-AwsExit "waiting for ALB deletion"

    Write-Host "ALB deleted."
}
else {
    Write-Host "ALB already absent."
}

Write-Host ""
Write-Host "[3/5] Discovering NAT Gateway from the private route table..."
$natId = aws ec2 describe-route-tables `
    --route-table-ids $PrivateRouteTableId `
    --profile $Profile `
    --region $Region `
    --no-cli-pager `
    --query "RouteTables[0].Routes[?DestinationCidrBlock=='0.0.0.0/0'].NatGatewayId | [0]" `
    --output text
Check-AwsExit "NAT discovery"

if (-not $natId -or $natId -eq "None") {
    Write-Host "No NAT Gateway referenced by the private route table."
}
else {
    Write-Host "Active route references NAT Gateway: $natId"

    $allocationId = aws ec2 describe-nat-gateways `
        --nat-gateway-ids $natId `
        --profile $Profile `
        --region $Region `
        --no-cli-pager `
        --query "NatGateways[0].NatGatewayAddresses[0].AllocationId" `
        --output text 2>$null

    $natDescribeExit = $LASTEXITCODE

    if ($natDescribeExit -eq 0) {
        Write-Host ""
        Write-Host "[4/5] Deleting NAT Gateway..."
        aws ec2 delete-nat-gateway `
            --nat-gateway-id $natId `
            --profile $Profile `
            --region $Region `
            --no-cli-pager | Out-Null
        Check-AwsExit "NAT Gateway deletion"

        aws ec2 wait nat-gateway-deleted `
            --nat-gateway-ids $natId `
            --profile $Profile `
            --region $Region
        Check-AwsExit "waiting for NAT Gateway deletion"

        Write-Host "NAT Gateway deleted."

        Write-Host ""
        Write-Host "[5/5] Releasing NAT Elastic IP..."
        if ($allocationId -and $allocationId -ne "None") {
            aws ec2 release-address `
                --allocation-id $allocationId `
                --profile $Profile `
                --region $Region
            Check-AwsExit "Elastic IP release"
            Write-Host "Released Elastic IP: $allocationId"
        }
        else {
            Write-Host "No Elastic IP allocation ID found."
        }
    }
    else {
        Write-Host "NAT Gateway no longer exists; nothing to delete."
    }
}

Write-Host ""
Write-Host "============================================================"
Write-Host "QuantMind is sleeping."
Write-Host "ECS desired count: 0"
Write-Host "ALB: deleted"
Write-Host "NAT Gateway: deleted"
Write-Host "NAT Elastic IP: released"
Write-Host ""
Write-Host "Persistent resources remain: VPC, subnets, route tables,"
Write-Host "security groups, target group, ECS service/cluster, ECR,"
Write-Host "IAM, S3 Vectors, and CloudWatch."
Write-Host "============================================================"
