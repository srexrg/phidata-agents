from phi.agent import Agent
from phi.tools.github import GithubTools

agent = Agent(
    instructions=[
        "Use your tools to answer questions and do tasks related to GitHub",
        "Do not create any issues or pull requests unless explicitly asked to do so",
    ],
    tools=[GithubTools()],
    show_tool_calls=True,
)
agent.print_response("Delete the repo called testing-phi", markdown=True)
