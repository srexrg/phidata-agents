from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

privacy_agent = Agent(
    name="Privacy Policy Agent",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGo()],
    instructions=[
        "You are a privacy policy analyzer. Your task is to find and analyze privacy policies for given tools or websites.",
        "When given a tool or website name, search for its privacy policy using DuckDuckGo.",
        "Once you find the privacy policy, summarize its key points and rate it on a scale of 1-10 for user-friendliness and data protection.",
        "Always include the source of the privacy policy in your response.",
    ],
    show_tool_calls=True,
    markdown=True,
)

privacy_agent.print_response("Analyze the privacy policy of Dropbox", stream=True)
