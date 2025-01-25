import streamlit as st
from phi.agent import Agent
from phi.model.ollama import Ollama

def create_agent():
    return Agent(
        model=Ollama(id="deepseek-r1", markdown=True),
        stream=True,
        system="You are a helpful assistant."
    )

def main():
    st.set_page_config(page_title="DeepSeek Chat Assistant", page_icon="🤖")

    st.title("🤖 DeepSeek Chat Assistant")
    st.markdown("Chat with an AI powered by DeepSeek. Enter your question below and get detailed responses!")

    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response
        agent = create_agent()

        try:
            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""

                for response in agent.run(prompt, stream=True):
                    print(response)
                    full_response += response.content
                    response_container.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
