from trello import TrelloClient
from trello_tool import TrelloTools
from phi.agent import Agent

trello_client = TrelloClient()

agent = Agent(
    instructions=[
        "You are a Trello management assistant that helps organize and manage Trello boards, lists, and cards",
        "Help users with tasks like:",
        "- Creating and organizing boards, lists, and cards",
        "- Moving cards between lists",
        "- Retrieving board and list information",
        "- Managing card details and descriptions",
        "Always confirm successful operations and provide relevant board/list/card IDs and URLs",
        "When errors occur, provide clear explanations and suggest solutions",
    ],
    tools=[TrelloTools(client=trello_client)],
    show_tool_calls=True,
)
agent.print_response(
    "Create a board called 'Test Board'",
    stream=True,
)
