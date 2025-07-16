"""
Module for fetching and processing ambulance service data in Hong Kong.

This module provides tools to retrieve and filter ambulance service indicators from the Fire Services Department.
"""

import csv
from datetime import datetime
from typing import Dict, List, Optional
from hkopenai_common.csv_utils import fetch_csv_from_url

from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the ambulance service tool with the FastMCP server."""

    @mcp.tool(
        description="Ambulance Service Indicators (Provisional Figures) in Hong Kong"
    )
    def get_ambulance_indicators(
        start_year: Annotated[int, Field(description="Start year of data range")],
        end_year: Annotated[int, Field(description="End year of data range")],
    ) -> List[Dict]:
        """
        Get Ambulance Service Indicators (Provisional Figures) in Hong Kong.

        Args:
            start_year: First year to include in results.
            end_year: Last year to include in results.

        Returns:
            List of monthly ambulance service indicators within the specified year range.
        """
        return _get_ambulance_indicators(start_year, end_year)


def _get_ambulance_indicators(
    start_year: Annotated[int, Field(description="Start year of data range")],
    end_year: Annotated[int, Field(description="End year of data range")],
) -> List[Dict]:
    """
    Get Ambulance Service Indicators (Provisional Figures) in Hong Kong.

    Args:
        start_year: First year to include in results.
        end_year: Last year to include in results.

    Returns:
        List of monthly ambulance service indicators within the specified year range.
    """
    url = "http://www.hkfsd.gov.hk/datagovhk/datasets/Ambulance_Service_Indicators_eng.csv"
    data = fetch_csv_from_url(url)
    filtered_data = []

    for row in data:
        date_str = row["Ambulance Service Indicators"]
        date = datetime.strptime(date_str, "%m/%Y")
        if start_year <= date.year <= end_year:
            filtered_data.append({"date": date_str, "data": row})
    return filtered_data
