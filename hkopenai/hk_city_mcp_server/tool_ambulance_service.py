"""
Module for fetching and processing ambulance service data in Hong Kong.

This module provides tools to retrieve and filter ambulance service indicators from the Fire Services Department.
"""

import csv
import urllib.request
from datetime import datetime
from typing import Dict, List

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




def fetch_ambulance_data() -> List[Dict]:
    """
    Fetch ambulance service data from Fire Services Department.

    Returns:
        List of dictionaries, each representing a row of ambulance service data.
    """
    url = "http://www.hkfsd.gov.hk/datagovhk/datasets/Ambulance_Service_Indicators_eng.csv"
    with urllib.request.urlopen(url) as response:
        lines = [l.decode("utf-8-sig") for l in response.readlines()]
    reader = csv.DictReader(lines)
    return list(reader)


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
    data = fetch_ambulance_data()
    filtered_data = []

    for row in data:
        date_str = row["Ambulance Service Indicators"]
        date = datetime.strptime(date_str, "%m/%Y")
        if start_year <= date.year <= end_year:
            filtered_data.append({"date": date_str, "data": row})
    return filtered_data
