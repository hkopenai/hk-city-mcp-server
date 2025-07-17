"""
Module for creating and running the HK City MCP Server.

This module provides functionality to configure and start the MCP server for HK OpenAI city data.
"""

from fastmcp import FastMCP

from .tools import ambulance_service


def server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI city Server")

    ambulance_service.register(mcp)

    return mcp
