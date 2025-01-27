from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.hackernews import HackerNews
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.tools.github import GithubTools
import os 

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

# Example usage
# personal_assistant.print_response(
#     "Crawl the website https://www.srexrg.me and summarize the content with urls if provided", stream=True
# )

personal_assistant.print_response(
    "Search for the repo local-loop and get the details of the repo where the user is srexrg", stream=True
)
