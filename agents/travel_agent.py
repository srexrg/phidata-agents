from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.exa import ExaTools
import os

exa_api_key = os.getenv("EXA__API_KEY")

itinerary_agent = Agent(
    name="Itinerary Planner",
    role="Planner",
    model=OpenAIChat(id="gpt-4o", ),
    tools=[ExaTools(api_key=exa_api_key)],
    description="You are an expert itinerary planning agent. Your role is to create detailed day-by-day travel plans.",
    instructions=[
        "Use Exa to find relevant information and suggestions for the itinerary from famous travel websites",
        "Create a clear and concise itinerary that includes a detailed day-by-day travel plan",
        "Suggest activity recommendations (e.g., sightseeing, dining, events)",
        "Provide estimated timings for each activity",
    ],
)

hotel_agent = Agent(
    name="Hotel Finder",
    role="Finder",
    model=OpenAIChat(id="gpt-4o", ),
    tools=[ExaTools(api_key=exa_api_key)],
    description="You are an expert hotel recommendation agent. Your role is to find suitable accommodations based on user preferences.",
    instructions=[
        "Use Exa to find relevant information and suggestions for hotels from popular booking websites",
        "Recommend hotels based on user preferences such as location, budget, and amenities",
        "Provide brief descriptions of recommended hotels",
        "Include estimated prices and availability information",
    ],
)

destination_agent = Agent(
    name="Destination Picker",
    role="Picker",
    model=OpenAIChat(id="gpt-4o", ),
    tools=[ExaTools(api_key=exa_api_key)],
    description="You are an expert destination recommendation agent. Your role is to suggest suitable travel destinations based on user preferences.",
    instructions=[
        "Use Exa to find relevant information and suggestions for destinations from popular travel websites",
        "Recommend destinations based on user preferences such as interests, budget, and travel style",
        "Provide brief descriptions of recommended destinations",
        "Include information on best times to visit and main attractions",
    ],
)

travel_team = Agent(
    team=[itinerary_agent, hotel_agent, destination_agent],
    model=OpenAIChat(id="gpt-4o", ),
    instructions=[
        "Work together to create a comprehensive travel plan for the user",
        "Start by picking a destination, then find suitable hotels, and finally create an itinerary",
        "Ensure all recommendations are aligned with user preferences and constraints",
    ],
    show_tool_calls=True,
    markdown=True,
)

travel_team.print_response(
    "I want to plan a 7-day trip to a beach destination in USA for a family of 4. Our budget is $5000. We enjoy water sports and local cuisine.",
    stream=True
)