from google.adk.agents.llm_agent import Agent
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERP_API_KEY")

def hotel_search_tool(location, check_in_date,check_out_date,adults, budget_tier = "medium"):
    url = "https://serpapi.com/search?engine=google_hotels"

    star_rating_map = {
            "low": "2,3",
            "medium": "3,4",
            "high": "4,5"
        }
    


    params = {
        "q": location,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date, # Corrected from check_in_date
            "adults": adults,
            "currency": "INR",
            "gl": "in",
            "hotel_class": star_rating_map.get(budget_tier, "3,4"),
            "sort_by": "3" if budget_tier == "low" else None,
            "api_key": api_key # Added api_key to params
    }

    params= {k: v for k,v in params.items() if v is not None}

    response = requests.get(url, params=params)

    if response.status_code !=200:
        print(response.text)
        return {"error": f"Failed to fetch data from API. Status code: {response.status_code}"}

    return response.json()





hotel_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_agent',
    description='A helpful agent to find hotels near the target location.',
    tools=[hotel_search_tool],
    output_key="hotel_search_results",
    instruction="""You are a hotel specialist. The user will provide:

        - check_in_date/trip_date (YYYY-MM-DD)
        - check_out_date/trip_date (YYYY-MM-DD)
        - location (city or area)

        Your task:
        1. You MUST calculate the check_in and check-out date based on the user's trip duration.
        2. Use the search_hotels tool to find accommodation.
        3. Search for hotels available between the given dates at the specified location. Use the hotel_search_tool.
        4. Return:
        - The best priced hotels
        - The lowest priced hotels
        - A list of all available hotels with pricing
        5. DO NOT include explanations or text outside JSON.
        6. Respond STRICTLY in valid JSON format.

        JSON Response Format:

        {
        "location": "",
        "check_in_date": "",
        "check_out_date": "",
        "lowest_price_hotels": [
            {
            "hotel_name": "",
            "price_per_night": 0,
            "total_price": 0,
            "currency": ""
            }
        ],
        "best_price_hotels": [
            {
            "hotel_name": "",
            "price_per_night": 0,
            "total_price": 0,
            "currency": "",
            "rating": 0
            }
        ],
        "all_hotels": [
            {
            "hotel_name": "",
            "price_per_night": 0,
            "total_price": 0,
            "currency": "",
            "rating": 0,
            "amenities": []
            }
        ]
        }

        If any field is missing or unknown, return an empty array or null. Output JSON only. If any tool returns status "error", explain the issue to the user clearly.
""",
)
