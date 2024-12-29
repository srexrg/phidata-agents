from phi.agent import Agent
from phi.model.groq import Groq
import os
from phi.tools.duckduckgo import DuckDuckGo

Groq_API_KEY = os.getenv("GROQ_API_KEY")
if not Groq_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY environment variable")

web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview",api_key=Groq_API_KEY),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)
web_agent.print_response("Who is Elon Musk ?", stream=True)
