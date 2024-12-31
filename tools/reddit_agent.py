import streamlit as st
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.reddit_tool import RedditTools


load_dotenv()


def create_agents():

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
            "6. Focus on authoritative and reliable sources"
    ]
)
    reddit_agent = Agent(
        name="Reddit Agent",
        role="Uploads post on Reddit",
        description="Specialized agent for crafting and publishing engaging Reddit posts",
        tools=[RedditTools(client_id="", client_secret="",username="", password="")],
        instructions=[
            "1. Get information regarding the subreddit",
            "2. Create attention-grabbing yet accurate titles",
            "3. Format posts using proper Reddit markdown",
            "4. Avoid including links ",
            "5. Follow subreddit-specific rules and guidelines",
            "6. Structure content for maximum readability",
            "7. Add appropriate tags and flairs if required"
            "8. Post the content to the subreddit"
        ],
        show_tool_calls=True,
    )
    post_team = Agent(
        team=[web_searcher, reddit_agent],
        instructions=[
            "Work together to create engaging and informative Reddit posts",
            "Start by researching the topic thoroughly using web searches",
            "Craft a well-structured post with accurate information and sources",
            "Follow Reddit guidelines and best practices for posting",
            "Upload the post to the specified subreddit",
            "Only complete execution after confirming successful post upload",
            "Return the post URL and status information"
        ],
        show_tool_calls=True,
        markdown=True
    )
    return post_team

def main():
    st.set_page_config(page_title="Reddit Post Creator", page_icon="📝")
    
    st.title("🤖 AI Reddit Post Creator Agent")
    st.markdown("This tool uses AI to help you create engaging Reddit posts. Simply enter the subreddit name, post topic, and type, and let the AI do the rest!")
    
    with st.form("reddit_form"):
        subreddit = st.text_input("Subreddit Name (without r/)", value="webdev")
        post_topic = st.text_area("Post Topic/Description")
        post_type = st.selectbox("Post Type", ["Text", "Discussion", "Question", "Guide"])
        
        submit = st.form_submit_button("Create Post")
    
    if submit:
        if not subreddit or not post_topic:
            st.error("Please fill in all required fields")
            return

        post_team = create_agents()
        if post_team is None:
            return

        try:
            with st.spinner("Creating your Reddit post..."):
                prompt = f"Create a {post_type.lower()} post about {post_topic} for the subreddit r/{subreddit}"
                
                with st.chat_message("assistant"):
                    response_container = st.empty()
                    full_response = ""
                    
                    for response in post_team.run(prompt, stream=True):
                        full_response += response.content
                        response_container.markdown(full_response)
                        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()