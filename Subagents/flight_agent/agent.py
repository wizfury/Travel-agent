from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERP_API_KEY")

def flight_search_tool(dep_id, arr_id, out_date, ret_date, adults):
    url = "https://serpapi.com/search?engine=google_flights"

    params = {
        "departure_id": dep_id,
        "arrival_id": arr_id,
        "outbound_date": out_date, 
        "return_date": ret_date,   
        "adults": adults,
        "currency": "INR",
        "api_key": api_key
    }

    params= {k: v for k,v in params.items() if v is not None}

    response = requests.get(url, params=params)

    if response.status_code !=200:
        return f"Error: {response.status_code} - {response.text}"

    return response.json()


flight_agent = Agent(
    model='gemini-2.5-flash',
    name='flight_agent',
    output_key="flight_search_results",
    # description='Find Flights matching the criteria.',
    instruction="""
            You are an intelligent flight-search assistant.

            Your responsibilities:
            1. Convert any given ORIGIN and DESTINATION city names into their correct IATA airport codes.
            - If a city has multiple airports, choose the main or most commonly used airport.
            - Examples:
                - "New York" → "JFK"
                - "London" → "LHR"
                - "Paris" → "CDG"
                - "Tokyo" → "HND"
            - If you cannot determine a code, set it to "".

            2. Search for available flights between the converted IATA codes. Use the flight_search_tool
            3. Curate:
            - The lowest-priced flight
            - The best-value flight (price + duration + stops + airline quality)
            - Top 5 cheapest flights

            STRICT RULES:
            - Output MUST be valid JSON.
            - NO text outside the JSON.
            - NO markdown.
            - DO NOT add extra fields.
            - All fields must be present even if empty.
            - Currency values must include symbols (e.g., "₹10,200").

            INPUT FORMAT:
            {
            "origin_city": "CITY NAME",
            "destination_city": "CITY NAME",
            "departure_date": "YYYY-MM-DD",
            "return_date": "YYYY-MM-DD or null"
            }

            OUTPUT FORMAT (STRICT JSON):
            {
            "origin_iata": "",
            "destination_iata": "",
            "available": true/false,
            "lowest_price_flight": {
                "airline": "",
                "price": "",
                "duration": "",
                "stops": "",
                "departure_time": "",
                "arrival_time": ""
            },
            "best_value_flight": {
                "airline": "",
                "price": "",
                "duration": "",
                "stops": "",
                "departure_time": "",
                "arrival_time": ""
            },
            "top_5_cheapest_flights": [
                {
                "airline": "",
                "price": "",
                "duration": "",
                "stops": "",
                "departure_time": "",
                "arrival_time": ""
                }
            ]
            }

            INSTRUCTIONS:
            - First convert the input cities to their correct IATA codes.
            - If the IATA codes are invalid or the city is unknown, set `"available": false`.
            - The final output must ONLY contain JSON. No commentary or explanations.
            - If any tool returns status "error", explain the issue to the user clearly.

            
            """,
    tools=[flight_search_tool]
)
