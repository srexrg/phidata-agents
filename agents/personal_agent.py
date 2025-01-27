from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.hackernews import HackerNews
from phi.model.openai import OpenAIChat
from phi.tools.calcom import CalCom
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.tools.github import GithubTools
from datetime import datetime


db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        "https://www.justice.gov/d9/criminal-ccips/legacy/2015/01/14/ccmanual_0.pdf",
    ],
    vector_db=PgVector(table_name="docs", db_url=db_url),
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
    team=[legal_agent, personal_assistant, calendar_agent],
    instructions=[
        "Use the LegalAdvisor for legal questions,PersonalAssistant for general tasks and CalendarAssistant for scheduling tasks.",
        "Always provide sources and use markdown formatting for better readability.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Example usage
# agent_team.print_response(
#     "Crawl the website https://www.srexrg.me and summarize the content with urls if provided", stream=True
# )

# agent_team.print_response(
#     "Search for the repo local-loop and get the details of the repo where the user is srexrg", stream=True
# )

# agent_team.print_response(
#     "What are the penalties for spoofing Email Address ?", stream=True
# )
agent_team.print_response(
    "Schedule a meeting on 28th January 2025 at 10:00 AM IST and add sreerag as the attendee mail id is sreeragp777@gmail.com", stream=True
)
