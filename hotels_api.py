API_KEYS = [
    "a477b74b1da2aa0544b2db6caabb6f26db513a5f4008b71ecbc0de3be7fef295",
    "d2c18f939fd4907412dfddec6b40d8b942c4117576995f0357460dac0dcd8b08",
    "2c475c83e591358c5437a96704d90112ebf08dd5136fccf7a9ca1e8ef321f340",
]

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import json



def search_hotels(
    query: str,
    check_in_date: str,
    check_out_date: str,
    adults: int = 2,
    children: int = 0,
    currency: str = "USD",
    language: str = "en",
    country: str = "us"
) -> Dict[str, Any]:
    """
    Search for hotels using Google Hotels API via SerpApi.
    
    Args:
        query: Search query for hotels (e.g. "Hotels in New York")
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        adults: Number of adults (default 2)
        children: Number of children (default 0)
        currency: Currency code (default USD)
        language: Language code (default en)
        country: Country code (default us)
        
    Returns:
        Dict containing hotel search results
    """
    
    # Validate dates
    try:
        datetime.strptime(check_in_date, "%Y-%m-%d")
        datetime.strptime(check_out_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")
        
    # Build API parameters
    params = {
        "engine": "google_hotels",
        "q": query,
        "gl": country,
        "hl": language,
        "currency": currency,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "children": children,
        "api_key": API_KEYS[0]
    }
    
    # Make API request
    response = requests.get(
        "https://serpapi.com/search",
        params=params
    )
    
    # Parse response
    try:
        results = response.json()
    except json.JSONDecodeError:
        raise Exception("Failed to decode API response")
        
    return results


if __name__ == "__main__":
    # Example usage
    query = "Hotels in New York"
    check_in_date = "2025-03-01"
    check_out_date = "2025-03-02"
    hotels = search_hotels(query, check_in_date, check_out_date)
    
    # print in json
    print(json.dumps(hotels, indent=4))
