from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
import streamlit as st

# Create the web search agent
web_agent = Agent(
    name="Coffee Shop Agent",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources when providing information about coffee shops."],
    show_tool_calls=True,
    markdown=True,
)

st.title("Coffee Shop Web Search Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What would you like to know about coffee shops?"):

    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for response in web_agent.run(prompt, stream=True):
            full_response += response.content
            response_container.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})