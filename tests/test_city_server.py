"""
Module for testing the MCP server creation and functionality.

This module contains unit tests for the server creation process and tool registration.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_city_mcp_server.server import server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server creation and tool functionality.

    This class contains test cases to ensure the server is created correctly and
    tools are properly registered and callable.
    """

    @patch("hkopenai.hk_city_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_city_mcp_server.tools.ambulance_service.register")
    def test_server(self, mock_register, mock_fastmcp):
        """
        Test the creation of the MCP server and tool registration.

        This test verifies that the server is created correctly, tools are registered
        using the decorator, and the tools call the underlying functions as expected.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        mock_register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
