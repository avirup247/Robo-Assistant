import google.generativeai as genai
import requests
import json

genai.configure(api_key="AIzaSyC7iL3_6o68GITllBAP9zFbXZfNXxJO6Iw")



API_KEY = "YOUR_APIKEY"
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}'

headers = {
    'Content-Type': 'application/json'
}
prompt="okay goodbye for now"
data = {
    "contents": {
        "role": "user",
        "parts": {
            "text": "okay goodbye for now"
        }
    },
    "tools": [
        {
            "function_declarations": [
                {
                    "name": "shutdown",
                    "description": "shutdown the system and not continuing the chat with user or ending the chat",
                },
                {
                    "name": "walk_forward",
                    "description": "start to walk or go in the forward direction to reach the user",
                    
                },
                {
                    "name": "walk_backward",
                    "description": "start to walk back or go in the backward direction from the user",
                    
                },
                {
                    "name": "capture_image",
                    "description": "click a image and store it inside database or to explain what in front of the model,the model capture image to see it.",
                    
                },
                {
                    "name": "get_showtimes",
                    "description": "Find the start times for movies playing in a specific theater",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA or a zip code e.g. 95616"
                            },
                            "movie": {
                                "type": "string",
                                "description": "Any movie title"
                            },
                            "theater": {
                                "type": "string",
                                "description": "Name of the theater"
                            },
                            "date": {
                                "type": "string",
                                "description": "Date for requested showtime"
                            }
                        },
                        "required": [
                            "location",
                            "movie",
                            "theater",
                            "date"
                        ]
                    }
                }
            ]
        }
    ]
}
response = requests.post(url,json=data)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
