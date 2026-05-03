import os
from openai import OpenAI
from agents.llm.base import BaseLLMClient

class OpenAIClient(BaseLLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def decide(self, user_input: str):
        prompt = f"""
Available tools:
get_flights
get_flight_by_id
create_booking
cancel_booking
get_bookings
create_user
get_user

Return only the best tool name.

User Request: {user_input}
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()