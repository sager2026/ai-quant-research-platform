import sys
from pathlib import Path

import pytest

from mcp import Client
from mcp.client.stdio import StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.anyio
async def test_external_stdio_mcp_tool_discovery():
    """
    Verify that QuantMind can run as a separate MCP server
    process and expose its tools over stdio transport.
    """

    server = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "app.presentation.mcp.server",
        ],
        cwd=str(PROJECT_ROOT),
    )

    async with Client(server) as client:
        tools = await client.list_tools()

        tool_names = [
            tool.name
            for tool in tools.tools
        ]

        assert "research_equity" in tool_names
