from phi.agent import Agent
from phi.tools.github import GithubTools
import streamlit as st


agent = Agent(
    instructions=[
        "Use your tools to answer questions asked related to Github ",
        "Do not create any issues or pull requests unless explicitly asked to do so",
    ],
    tools=[GithubTools()],
    markdown=True,
)

st.title("Github Repository Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What would you like to know about github repositories?"):

    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for response in agent.run(prompt, stream=True):
            full_response += response.content
            response_container.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})