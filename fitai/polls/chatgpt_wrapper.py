import requests
import json
from django.conf import settings

API_URL = "https://api.openai.com/v1/chat/completions"

def generate_chat_gpt_response(messages, unique_users=None, tokens=500, temperature=0.7):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": tokens,
        "temperature": temperature,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    if unique_users:
        data["user"] = unique_users

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"].strip()
    else:
        return f"An error occurred while making the API call: {response.text}"

def generate_workout_routine(fitness_data):
    messages = [
        {"role": "user", "content": f"Create a workout routine based on the following fitness data: {fitness_data}"},
    ]

    response = generate_chat_gpt_response(messages, tokens=500, temperature=0.7)
    return response
