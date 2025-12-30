from google.adk.agents.llm_agent import Agent
from google.adk.agents import ParallelAgent,SequentialAgent, LlmAgent
from Travel_agent.Subagents.flight_agent.agent import flight_agent
from Travel_agent.Subagents.hotel_agent.agent import hotel_agent
from Travel_agent.Subagents.itiniary_agent.agent import itiniary_agent


research_team = ParallelAgent(
    name= "ResearchTeam",
    sub_agents=[flight_agent, hotel_agent,itiniary_agent],
)

aggregator_agent = Agent(
    name="TravelAggregator",
    # Using the configuration style you requested
    model='gemini-2.5-flash', 
    
    # The instruction uses placeholders that match the 'output_key' 
    # of your previous agents exactly.
    instruction="""
    You are the Senior Travel Architect. Create a finalized trip proposal based on the research team's findings.

    **Flight Research Data:**
    {flight_search_results}
    
    **Hotel Research Data:**
    {hotel_search_results}
    
    **Your Task:**
    1. Compare the flight options. Select the 'best_value_flight' as the default choice.
    2. Compare the hotel options. Select the best hotel based on the user's budget tier (inferred from hotel prices).
    3. detailed_itinerary: Create a logical daily plan.
    4. summary: Write a brief 100-word executive summary of the trip cost and vibe.
    """,
)

print("✅ aggregator_agent created.")

trip_orchestrator = SequentialAgent(
    name="trip_orchestrator",
    sub_agents=[research_team, aggregator_agent]
)

root_agent = Agent(
    name="UserInteractionAgent",
    model='gemini-2.5-flash',
    instruction="""
    You are the User Interface for the Travel Agent system.
    Your goal is to converse with the user to gather all necessary details to plan a trip.
    
    Required Information:
    1. Origin City (Where are they flying from?)
    2. Destination City (Where are they going?)
    3. Departure Date (YYYY-MM-DD or clear date)
    4. Return Date (YYYY-MM-DD or clear date)
    5. Number of Travelers (Adults)
    
    Status Checks:
    - If ANY of these pieces of information is missing, you must ASK the user for them.
    - Do NOT make up information.
    - If the user provides a vague date (e.g., "next week"), verify the specific dates.

    STRICT COMMUNICATION RULES:
    - Never mention function names, tool names, or internal variable names (e.g., 'trip_orchestrator', 'UserInteractionAgent', 'flight_search_tool').
    - Speak naturally and professionally.
    - Do not explain your internal process (e.g., "I will now call the sub-agent"). Just say "I'm starting the search for you now," or similar.

    Termination/Delegation:
    - ONLY when you have ALL 5 pieces of information, you should invoke the 'trip_orchestrator' sub-agent.
    - Pass the collected information clearly to the 'trip_orchestrator'.
    """,
    sub_agents=[trip_orchestrator]
)
