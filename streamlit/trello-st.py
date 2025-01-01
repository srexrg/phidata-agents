import os
from tools.trello_tool import TrelloTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.agent import Agent
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

trello = TrelloTools(
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("secret"),
    token=os.getenv("token"),
)


web_searcher = Agent(
    name="Web Searcher",
    role="Searches the web for information on a topic",
    description="An intelligent agent that performs comprehensive web searches to gather current and accurate information",
    tools=[DuckDuckGo()],
    instructions=[
        "1. Perform focused web searches using relevant keywords",
        "2. Filter results for credibility and recency",
        "3. Extract key information and main points",
        "4. Organize information in a logical structure",
        "5. Verify facts from multiple sources when possible",
        "6. Focus on authoritative and reliable sources",
    ],
)
trello_agent = Agent(
    name="Trello Agent",
    description="Specialized agent for doing task related to trello",
    instructions=[
        "You are a Trello management assistant that helps organize and manage Trello boards, lists, and cards",
        "Help users with tasks like:",
        "- Creating and organizing boards, lists, and cards",
        "- Moving cards between lists",
        "- Retrieving board and list information",
        "- Managing card details and descriptions",
        "Always confirm successful operations and provide relevant board/list/card IDs and URLs",
        "When errors occur, provide clear explanations and suggest solutions",
    ],
    tools=[trello],
    show_tool_calls=True,
)


def create_agents():
    task_team = Agent(
        team=[web_searcher, trello_agent],
        instructions=[
            "Work together to manage Trello tasks with web-informed decisions",
            "1. Use web_searcher to research topics when additional context is needed",
            "2. Use trello_agent to perform Trello board management tasks",
            "3. Coordinate between agents to make informed decisions about task organization",
            "4. Verify successful completion of Trello operations",
            "5. Provide clear feedback about actions taken and any relevant URLs or IDs",
        ],
        show_tool_calls=True,
        markdown=True,
    )
    return task_team


def main():
    st.set_page_config(page_title="Trello Task Manager", page_icon="📋")

    st.title("🤖 AI Trello Task Manager")
    st.markdown(
        """This AI-Agent helps you research topics and automatically organize them in Trello."""
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to do with Trello?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        task_team = create_agents()

        try:
            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""

                for response in task_team.run(prompt, stream=True):
                    full_response += response.content
                    response_container.markdown(full_response)

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
