from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TAVLY_API_KEY")

import requests

def search_activities(city):
    url = "https://api.tavily.com/search"
    
    payload = {
        "query": f"top tourist activities and attractions in {city}", 
        "topic": "general",
        "search_depth": "basic",
        "max_results": 3,
        "time_range": None,
        "days": 3,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }

    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information from results
        activities = []
        for result in data.get("results", []):
            activity = {
                "title": result.get("title"),
                "description": result.get("content"),
                "url": result.get("url"),
                "image": result.get("image_url")
            }
            activities.append(activity)
            
        return activities
        
    except requests.exceptions.RequestException as e:
        print(f"Error searching activities: {str(e)}")
        return []

if __name__ == "__main__": 
    activities = search_activities("Cracow")
    print(activities)

