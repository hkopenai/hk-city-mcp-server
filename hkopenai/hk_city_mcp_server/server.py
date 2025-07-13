"""
Module for creating and running the HK City MCP Server.

This module provides functionality to configure and start the MCP server for HK OpenAI city data.
"""

from fastmcp import FastMCP

import hkopenai.hk_city_mcp_server.tool_ambulance_service


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI city Server")

    hkopenai.hk_city_mcp_server.tool_ambulance_service.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to run the MCP Server.

    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(
            f"MCP Server started in SSE mode on port {port}, bound to {host}"
        )
    else:
        server.run()
        print("MCP Server running in stdio mode")
