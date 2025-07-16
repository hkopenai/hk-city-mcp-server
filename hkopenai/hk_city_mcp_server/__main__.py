"""
Main entry point for the HK City MCP Server.

This module serves as the entry point to run the HK City MCP Server application.
It handles command-line arguments and initiates the main server functionality.
"""

from hkopenai_common.cli_utils import cli_main
from .server import create_mcp_server

if __name__ == "__main__":
    cli_main(create_mcp_server, "HK City MCP Server")
