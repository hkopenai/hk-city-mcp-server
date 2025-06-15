import urllib.request
import csv
from io import StringIO
from typing import List, Dict
from pydantic import Field
from typing_extensions import Annotated
from datetime import datetime

def fetch_ambulance_data() -> List[Dict]:
    """Fetch ambulance service data from Fire Services Department"""
    url = "http://www.hkfsd.gov.hk/datagovhk/datasets/Ambulance_Service_Indicators_eng.csv"
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8-sig') for l in response.readlines()]
    reader = csv.DictReader(lines)
    return list(reader)

def get_ambulance_indicators(
    start_year: Annotated[int, Field(description="Start year of data range")],
    end_year: Annotated[int, Field(description="End year of data range")]
) -> List[Dict]:
    """Get Ambulance Service Indicators (Provisional Figures) in Hong Kong
    
    Args:
        start_year: First year to include in results
        end_year: Last year to include in results
    
    Returns:
        List of monthly ambulance service indicators within the specified year range
    """
    data = fetch_ambulance_data()
    filtered_data = []
    
    for row in data:
        date_str = row['Ambulance Service Indicators']
        date = datetime.strptime(date_str, '%m/%Y')
        if start_year <= date.year <= end_year:
            filtered_data.append({ 'date': date_str, 'data': row})
    return filtered_data
