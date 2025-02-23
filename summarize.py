from dotenv import load_dotenv  # Import load_dotenv
import os
import requests

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"    
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def summarize(transcript, selected_flights, selected_hotels, activities):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    conversation_history = [
        {
            "role": "system",
            "content": """
You are an AI that receives a transcript, selected flights, selected hotels and list of activities and your task is to create a summary of the conversation. The summary should be in a natural language and should be concise and to the point. It should be long, explaining the reasoning that was behind the choice. 

The response should be in a JSON format like this:
- title - "<place some emoji here that is relevant to the chat> Trip to <city>"
- summary - summarize the flights, hotel and activities and put them here.
- city - the city where use is going, for example "New York"
"""
        },
        {"role": "user", "content": transcript},
        {"role": "user", "content": selected_flights},
        {"role": "user", "content": selected_hotels},
        {"role": "user", "content": activities}
    ]

    payload = {
        "messages": conversation_history,
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.6,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "response_format": { "type": "json_object" },
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    return response.json()



if __name__ == "__main__":
    transcript = """
[{'role': 'assistant', 'content': 'Hey, how can i help you?'}, {'role': 'user', 'content': 'I would like to book a flight from Warsaw to New York.'}, {'role': 'assistant', 'content': 'Okay, I can help you with that. What date would you like to fly?\n'}, {'role': 'user', 'content': 'March 2nd, 2025.'}, {'role': 'assistant', 'content': 'Okay, and would you like to book a return flight as well?\n'}, {'role': 'user', 'content': 'No, thank you.'}, {'role': 'assistant', 'content': 'Please give me a few moments to look into this.\n'}, {'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': 'I found three flights for you. The first option is with LOT. It departs Warsaw Frederic Chopin at four fifty p.m. and arrives at John F. Kennedy International Airport at eight thirty-five p.m. The price is seven hundred and thirty-two. The second option is with SWISS. It departs Warsaw Frederic Chopin at nine forty-five a.m. and arrives at John F. Kennedy International Airport at four forty p.m. The price is one thousand and twelve. The third option is with Air France. It departs Warsaw Frederic Chopin at six thirty-five a.m. and arrives at John F. Kennedy International Airport at one p.m. The price is one thousand one hundred and thirty-six. Which flight do you prefer?\n'}, {'role': 'user', 'content': 'The first one.'}, {'role': 'assistant', 'content': 'Okay, the LOT flight. One moment.\n'}, {'role': 'assistant', 'content': 'Okay, your flight has been selected. Is there anything else I can help you with? Perhaps a hotel booking?\n'}, {'role': 'user', 'content': "No, that's all. Thank you."}, {'role': 'assistant', 'content': 'Happy I could help with your flight booking! Have a wonderful day!'}]
"""
    selected_flights = """
[{"flights":[{"airline":"LOT","arrival_airport":{"id":"JFK","name":"John F. Kennedy International Airport","time":"2025-03-02 20:35"},"departure_airport":{"id":"WAW","name":"Warsaw Frederic Chopin","time":"2025-03-02 16:50"},"duration":585,"flight_number":"LO 26"}]"""
    selected_hotels = "None"
    activities = """
[{'title': '25 Most Visited Tourist Attractions in New York City (Ranked)', 'description': 'Famous for its luxury stores (it’s the most expensive shopping street in the world) and historic buildings, Fifth Avenue is a great place to start this list of the best tourist attractions in New York City. Averaging 6 million visitors per year, it’s also one of the most popular tourist attractions in New York City. In fact, this the third most popular tourist attraction in New York City (after Central Park and Times Square). The bright buildings make Times Square not only one of the best tourist attractions in New York City, but of the entire world. Central Park is also one of the most famous tourist attractions in New York City because it’s ripe with photo-taking locations.', 'url': 'https://newyorksimply.com/nyc-tourist-attractions-new-york-city/', 'image': None}, {'title': '22 Top-Rated Tourist Attractions in New York City - PlanetWare', 'description': '22 Top-Rated Tourist Attractions in New York City Some people come here to enjoy the Broadway shows; others come specifically to shop; and many come simply to see the tourist attractions: the Statue of Liberty, the Empire State Building, Brooklyn Bridge, Central Park, historic neighborhoods, and world-famous museums. Read More: Best Parks in New York City Read More: Top-Rated Museums in New York City The best area runs from approximately the south end of Central Park to the New York Public Library, or more specifically, between 60th Street and 40th Street. 17 Top-Rated Museums in New York City 20 Best Cities in New York 17 Best Parks in New York City', 'url': 'https://www.planetware.com/tourist-attractions-/new-york-city-us-ny-nyc.htm', 'image': None}, {'title': '87 Best Attractions in New York for 2025 - Time Out', 'description': "Discover the New York attractions locals love including historical landmarks, stunning NYC parks and more. The list is a compilation of our favorite sights and spots in the city, including everything from great\xa0parks\xa0and\xa0art museums, to food markets and historical venues. Let the world believe the Empire State Building has the best view of New York City–it keeps the crowds slightly more manageable at 30 Rockefeller Center’s spectacular open air observation deck. Built in 1804, it's the oldest museum in New York City. Opened in 2004, this six-story museum (once home to Barneys New York) houses Donald and Shelley Rubin’s impressive collection of Himalayan art and artifacts, as well as large-scale temporary exhibitions.", 'url': 'https://www.timeout.com/newyork/attractions/new-york-attractions', 'image': None}]"""
    print(summarize(transcript, selected_flights, selected_hotels, activities))

    
