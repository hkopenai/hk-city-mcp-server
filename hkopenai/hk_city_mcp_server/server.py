"""
Module for creating and running the HK City MCP Server.

This module provides functionality to configure and start the MCP server for HK OpenAI city data.
"""

import argparse
from fastmcp import FastMCP
from typing import Dict, List, Annotated, Optional
import hkopenai.hk_city_mcp_server.tool_ambulance_service
from pydantic import Field


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI city Server")

    hkopenai.hk_city_mcp_server.tool_ambulance_service.register(mcp)

    return mcp


def main(args):
    """
    Main function to run the MCP Server.

    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http", host=args.host, port=args.port)
        print(
            f"MCP Server started in SSE mode on port {args.port}, bound to {args.host}"
        )
    else:
        server.run()
        print("MCP Server running in stdio mode")
