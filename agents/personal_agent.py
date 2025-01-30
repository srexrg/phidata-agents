from phi.agent import Agent
import streamlit as st
import os
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.hackernews import HackerNews
from phi.model.openai import OpenAIChat
from phi.tools.calcom import CalCom
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.tools.github import GithubTools
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.tools.reddit import RedditTools
from datetime import datetime

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        "https://www.justice.gov/d9/criminal-ccips/legacy/2015/01/14/ccmanual_0.pdf",
    ],
    vector_db=PgVector(table_name="docs", db_url=db_url),
)

arxiv_agent = Agent(
    name="Arxiv Agent",
    tools=[ArxivToolkit()],
    description="You are a research assistant specializing in scientific publications from ArXiv.",
    instructions=[
        "For a given topic or query, search ArXiv for relevant publications.",
        "Analyze the results and provide a summary of the most relevant findings.",
        "Include titles, authors, and brief descriptions of the top papers.",
        "Provide insights on the current state of research in the given area.",
    ],
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
)

reddit_agent = Agent(
    name="Reddit Agent",
    tools=[RedditTools(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, username=REDDIT_USERNAME, password=REDDIT_PASSWORD)],
    instructions=[
        "You are a Reddit Agent that can:",
        "- Search and browse subreddits",
        "- Fetch posts, comments, and discussions",
        "- Get trending topics and popular content",
        "- Retrieve user information and post history",
        "- Create posts when requested",
        "- Monitor specific subreddits for updates",
        "Always provide context and source links when sharing information",
        "Format responses using proper Reddit markdown for readability",
    ],
    show_tool_calls=True,
    markdown=True,
)

legal_agent = Agent(
    name="LegalAdvisor",
    knowledge=knowledge_base,
    search_knowledge=True,
    model=OpenAIChat(id="gpt-4o"),
    markdown=True,
    instructions=[
        "Provide legal information and advice based on the knowledge base.",
        "Include relevant legal citations and sources when answering questions.",
        "Always clarify that you're providing general legal information, not professional legal advice.",
        "Recommend consulting with a licensed attorney for specific legal situations.",
    ],
    show_tool_calls=True,
)

calendar_agent = Agent(
    name="Calendar Assistant",
    instructions=[
        f"You're scheduing assistant. Today is {datetime.now()}.",
        "You can help users by:",
        "- Finding available time slots",
        "- Creating new bookings",
        "- Managing existing bookings (view, reschedule, cancel) ",
        "- Getting booking details",
        "- IMPORTANT: In case of rescheduling or cancelling booking, call the get_upcoming_bookings function to get the booking uid. check available slots before making a booking for given time",
        "Always confirm important details before making bookings or changes.",
    ],
    model=OpenAIChat(id="gpt-4o"),
    tools=[CalCom(user_timezone="Asia/Kolkata")],
    show_tool_calls=True,
    markdown=True,
)


personal_assistant = Agent(
    name="Personal Assistant",
    tools=[
        DuckDuckGo(),
        YFinanceTools(),
        HackerNews(),
        Crawl4aiTools(),
        GithubTools(),
    ],
    description="I am your personal AI assistant, capable of helping with various tasks.",
    instructions=[
        "Use web search for general queries.",
        "Provide financial data and analysis when requested.",
        "Share top stories from HackerNews when asked about tech news.",
        "Use the web crawler if asked to summarize or scrape a website.",
        "Use the github tool if asked to search or do tasks related to github"
        "Always provide sources for information.",
        "Use markdown formatting for better readability.",
    ],
    show_tool_calls=True,
    markdown=True,
    add_datetime_to_instructions=True,
)

agent_team = Agent(
    team=[legal_agent, personal_assistant, calendar_agent,arxiv_agent,reddit_agent],
    instructions=[
        "Use the LegalAdvisor for legal questions,PersonalAssistant for general tasks and CalendarAssistant for scheduling tasks.Use RedditAgent for things related to reddit.",
        "Use ArxivAgent for things related to arxiv.",
        "Always provide sources and use markdown formatting for better readability.",
    ],
    show_tool_calls=True,
    add_chat_history_to_messages=True,
    num_history_responses=3,
    markdown=True,
)


st.set_page_config(page_title="AI Agent Team", page_icon="🤖", layout="wide")


with st.sidebar:
    st.title("🤖 AI Agent Team")
    st.markdown(
        """
    This AI team consists of:
    - 👨‍⚖️ **Legal Advisor** - For legal information and advice
    - 📅 **Calendar Agent** - For scheduling and managing appointments
    - 🌟 **Personal Agent** - For general tasks, finance, and tech news
    """
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

st.title("💬 Chat with AI Agent Team")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(
        message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"
    ):
        st.markdown(message["content"])


if prompt := st.chat_input("How can I help you today?"):

    st.divider()

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        response_container = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            for response in agent_team.run(prompt, stream=True):
                full_response += response.content
                response_container.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
