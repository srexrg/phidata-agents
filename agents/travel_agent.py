import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.exa import ExaTools
import os

# Initialize session states
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

def create_agents():
    exa_api_key = os.getenv("EXA_API_KEY")
    if not exa_api_key:
        st.error("EXA API key not found. Please set the EXA_API_KEY environment variable.")
        return None
    
    try:
        itinerary_agent = Agent(
            name="Itinerary Planner",
            role="Planner",
            model=OpenAIChat(id="gpt-4o"),
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
            model=OpenAIChat(id="gpt-4o"),
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
            model=OpenAIChat(id="gpt-4o"),
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
            model=OpenAIChat(id="gpt-4o"),
            instructions=[
                "Work together to create a comprehensive travel plan for the user",
                "Start by picking a destination, then find suitable hotels, and finally create an itinerary",
                "Ensure all recommendations are aligned with user preferences and constraints",
            ],
            show_tool_calls=True,
            markdown=True,
        )
        
        return travel_team
    except Exception as e:
        st.error(f"Error creating agents: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Travel Planner", page_icon="✈️", layout="wide")
    
    st.title("🌴 AI Travel Planner")
    
    # Input form
    with st.form("travel_form"):
        duration = st.number_input("Trip Duration (days)", min_value=1, max_value=30, value=7)
        destination_type = st.selectbox("Destination Type", ["Beach", "Mountain", "City", "Countryside"])
        location = st.selectbox("Location", ["USA", "Europe", "Asia", "Africa", "South America"])
        budget = st.number_input("Budget ($)", min_value=1000, value=5000)
        travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=2)
        interests = st.multiselect(
            "Interests",
            ["Water Sports", "Local Cuisine", "History", "Shopping", "Nature", "Adventure", "Culture"]
        )
        
        submit = st.form_submit_button("Plan My Trip")
    
    if submit:
        if not interests:
            st.error("Please select at least one interest.")
            return

        travel_team = create_agents()
        if not travel_team:
            return
        
        # Create prompt from form inputs
        prompt = f"""I want to plan a {duration}-day trip to a {destination_type.lower()} destination in {location} for a group of {travelers}. 
        Our budget is ${budget}. We enjoy {', '.join(interests).lower()}."""
        
        try:
            with st.spinner("Planning your perfect trip..."):
                st.chat_message("user").markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("assistant"):
                    response_container = st.empty()
                    full_response = ""
                    for response in travel_team.run(prompt, stream=True):
                        full_response += response.content
                        response_container.markdown(full_response)

                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.session_state.responses.append(full_response)

        except Exception as e:
            st.error(f"An error occurred while planning your trip: {str(e)}")

if __name__ == "__main__":
    main()