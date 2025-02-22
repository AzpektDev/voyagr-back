API_KEYS = [
    "a477b74b1da2aa0544b2db6caabb6f26db513a5f4008b71ecbc0de3be7fef295",
    "d2c18f939fd4907412dfddec6b40d8b942c4117576995f0357460dac0dcd8b08",
    "2c475c83e591358c5437a96704d90112ebf08dd5136fccf7a9ca1e8ef321f340",
]

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import json

def search_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: Optional[str] = None,
    currency: str = "USD",
    language: str = "en",
    country: str = "us"
) -> Dict[str, Any]:
    """
    Search for flights using the Google Flights API via SerpApi.
    
    Args:
        departure_id: Departure airport code (e.g. 'CDG' for Paris)
        arrival_id: Arrival airport code (e.g. 'JFK' for New York)
        outbound_date: Departure date in YYYY-MM-DD format
        return_date: Optional return date in YYYY-MM-DD format
        currency: Currency code (default 'USD')
        language: Language code (default 'en')
        country: Country code (default 'us')
    
    Returns:
        Dict containing flight search results
    """
    # Validate date format
    try:
        datetime.strptime(outbound_date, '%Y-%m-%d')
        if return_date:
            datetime.strptime(return_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")

    # Base URL for the API
    url = "https://serpapi.com/search"

    # Build parameters
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": currency,
        "hl": language,
        "gl": country,
        "api_key": API_KEYS[0]  # Using first API key
    }

    # Add return date if provided
    if return_date:
        params["return_date"] = return_date
        params["type"] = "1"  # Round trip
    else:
        params["type"] = "2"  # One way

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        return response.json()
        
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch flight data: {str(e)}")


def prepare_flight_search_response(flight_details):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    conversation_history = [
        {
            "role": "system",
            "content": "You are a flight search API. You will receive flight booking details and should return a consistent JSON response with available flight options. Always return exactly 3 flight options with fixed prices and times, formatted as an array of flight objects."
        },
        {
            "role": "user",
            "content": json.dumps(flight_details)    
        }
    ]

    payload = {
        "messages": conversation_history,
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.1,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]  





if __name__ == "__main__":
    # Example usage
    departure_id = "WAW"
    arrival_id = "JFK"
    outbound_date = "2025-03-01"
    return_date = "2025-03-05"
    
    try:
        flights = search_flights(departure_id, arrival_id, outbound_date, return_date)
        # print(flights['best_flights']
        flight_search_response = prepare_flight_search_response(flights['best_flights'])
        print(flight_search_response)


        # print(flights)

        # prettify json
        # print(json.dumps(flights, indent=4))


        # save json to file
    #     with open("flights.json", "w") as f:
    #         json.dump(flights, f, indent=4)
    except Exception as e:
        print(f"Error: {e}")

