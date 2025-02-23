# first attempt before we discovered conversational ai from elevenlabs 💀
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"


def prepare_flight_json(user_response):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    conversation_history = [
        {
            "role": "system",
            "content": "You're an AI that receives sentence about user trying to book the plane, sentence should have destination, origin airport, starting and ending trip. Before sending any JSON, make sure that it contains all the data. If not return error equal to true, and short message about what went wrong. If you received all data, return those things as \n- \"origin\" airport code of origin\n- \"date_start\" start of the trip\n- \"date_end\" end of the trip\n- \"destination\" airport code of destination\nIf possible, get airport code for the destination. For example WAW warsaw, WMI is warsaw modlin airport"
        },
        {"role": "user", "content": user_response},
    ]
    
    payload = {

        "messages": conversation_history,
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.6,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "response_format": { "type": "json_object" },
    }

    response = requests.post(GROQ_API_URL, 
                           headers=headers,
                           json=payload)
    return response

def prepare_human_response(json_response):
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    conversation_history = [
        {
            "role": "system",
            "content": "You are a helpful AI that converts flight booking details into natural language. You will receive JSON with flight details including origin airport code, destination airport code, start date and end date. Convert this into a friendly, natural response confirming the booking details."
        },
        {
            "role": "user",
            "content": str(json_response)
        },
    ]

    payload = {
        "messages": conversation_history,
        "model": "llama-3.3-70b-versatile", 
        "temperature": 0.7,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
    }

    response = requests.post(GROQ_API_URL,
                           headers=headers, 
                           json=payload)
    return response.json()["choices"][0]["message"]["content"]



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
            "content": str(flight_details)
        }
    ]

    payload = {
        "messages": conversation_history,
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.1, # Low temperature for consistent responses
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(GROQ_API_URL,
                           headers=headers,
                           json=payload)
    return response.json()["choices"][0]["message"]["content"]




if __name__ == "__main__":
    print("Welcome! Where do you want to go?")
    user_response = input(">> ")

    flight_json = prepare_flight_json(user_response)
    flight_json = flight_json.json()

    flight_search_response = prepare_flight_search_response(flight_json)

    human_response = prepare_human_response(flight_search_response)
    print(human_response)





    
    # response = prepare_flight_json(user_response)
    # response = response.json()
    # print(response["choices"][0]["message"]["content"])
    # example response:
    # {
    #    "origin": "WAW",
    #    "date_start": "2024-05-02",
    #    "date_end": "2024-05-04",
    #    "destination": "BER"
    #}