import requests

def make_request():
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_API_KEY = "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"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    conversation_history = [
        {
            "role": "system",
            "content": "You're an AI that receives sentence about user trying to book the plane, sentence should have destination, origin airport, starting and ending trip. Before sending any JSON, make sure that it contains all the data. If not return error equal to true, and short message about what went wrong. If you received all data, return those things as \n- \"origin\" airport code of origin\n- \"date_start\" start of the trip\n- \"date_end\" end of the trip\n- \"destination\" airport code of destination\nIf possible, get airport code for the destination. For example WAW warsaw, WMI is warsaw modlin airport"
        },
        {"role": "user", "content": "I want to go from warsaw to berlin. I want to go 2nd of may and return after 2 days"},
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

if __name__ == "__main__":
    response = make_request()
    response = response.json()
    print(response["choices"][0]["message"]["content"])
    # example response:
    # {
    #    "origin": "WAW",
    #    "date_start": "2024-05-02",
    #    "date_end": "2024-05-04",
    #    "destination": "BER"
    #}