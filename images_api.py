import requests
from typing import Dict, Any
import json

API_KEYS = [
    "a477b74b1da2aa0544b2db6caabb6f26db513a5f4008b71ecbc0de3be7fef295",
    "d2c18f939fd4907412dfddec6b40d8b942c4117576995f0357460dac0dcd8b08",
    "2c475c83e591358c5437a96704d90112ebf08dd5136fccf7a9ca1e8ef321f340",
]

def search_city_image(city: str, num_images: int = 1) -> Dict[str, Any]:
    params = {
        "engine": "google_images",
        "q": f"{city} panorama skyline",
        "num": num_images,
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
    city = "Warsaw"
    images = search_city_image(city)
    
    # Print in JSON format
    # print(json.dumps(images, indent=4))

    print(images["images_results"][0]["original"])
