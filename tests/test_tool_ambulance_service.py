"""
Module for testing the ambulance service indicators tool.

This module contains unit tests for fetching and filtering ambulance service data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_city_mcp_server.tool_ambulance_service import _get_ambulance_indicators
from hkopenai.hk_city_mcp_server.tool_ambulance_service import register


class TestAmbulanceService(unittest.TestCase):
    """
    Test class for verifying ambulance service indicators functionality.

    This class contains test cases to ensure the data fetching and filtering
    for ambulance service indicators work as expected.
    """

    def test_get_ambulance_indicators(self):
        """
        Test the retrieval and filtering of ambulance service indicators.

        This test verifies that the function correctly filters data by year range,
        returns empty results for non-matching years, and handles partial year matches.
        """
        # Mock the CSV data
        mock_csv_data = [
            {
                "Ambulance Service Indicators": "01/2019",
                "no. of emergency calls": "70004",
                "no. of hospital transfer calls": "4970",
                "calls per ambulance": "200.70",
                "turnouts of ambulances, ambulance motor cycles and Rapid Response Vehicles to calls": "78137",
                "emergency move-ups of ambulances to provide operational coverage": "8186",
            },
            {
                "Ambulance Service Indicators": "02/2019",
                "no. of emergency calls": "57701",
                "no. of hospital transfer calls": "4104",
                "calls per ambulance": "172.87",
                "turnouts of ambulances, ambulance motor cycles and Rapid Response Vehicles to calls": "63926",
                "emergency move-ups of ambulances to provide operational coverage": "7143",
            },
            {
                "Ambulance Service Indicators": "01/2020",
                "no. of emergency calls": "62991",
                "no. of hospital transfer calls": "4186",
                "calls per ambulance": "177.45",
                "turnouts of ambulances, ambulance motor cycles and Rapid Response Vehicles to calls": "67363",
                "emergency move-ups of ambulances to provide operational coverage": "9364",
            },
        ]

        with patch(
            "hkopenai.hk_city_mcp_server.tool_ambulance_service.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test filtering by year range
            result = _get_ambulance_indicators(2019, 2019)
            self.assertEqual(len(result), 2)

            # Test empty result for non-matching years
            result = _get_ambulance_indicators(2021, 2022)
            self.assertEqual(len(result), 0)

            # Test partial year match
            result = _get_ambulance_indicators(2019, 2020)
            self.assertEqual(len(result), 3)

    def test_register_tool(self):
        """
        Test the registration of the get_ambulance_indicators tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_ambulance_indicators function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Ambulance Service Indicators (Provisional Figures) in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_ambulance_indicators")

        # Call the decorated function and verify it calls _get_ambulance_indicators
        with patch(
            "hkopenai.hk_city_mcp_server.tool_ambulance_service._get_ambulance_indicators"
        ) as mock_get_ambulance_indicators:
            decorated_function(start_year=2018, end_year=2019)
            mock_get_ambulance_indicators.assert_called_once_with(2018, 2019)
