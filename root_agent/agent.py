from google.adk.agents.llm_agent import Agent
from google.adk.agents import ParallelAgent,SequentialAgent, LlmAgent
from Subagents.flight_agent.agent import flight_agent
from Subagents.hotel_agent.agent import hotel_agent
from Subagents.itiniary_agent.agent import itiniary_agent

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

root_agent = SequentialAgent(
    name="trip_orchestrator",

    sub_agents=[research_team, aggregator_agent])
