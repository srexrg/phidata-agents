import os
from trello_tool import TrelloTools
from phi.agent import Agent
from dotenv import load_dotenv

load_dotenv()

trello = TrelloTools(
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("secret"),
    token=os.getenv("token")
)


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
    tools=[trello],
    show_tool_calls=True,
)

agent.print_response("inside the board my-project-board move card agent sir from todo list to 'New list' ", stream=True)


# board_response = trello.create_board(
#     name="My Project Board",
#     description="Board for tracking project tasks",
#     default_lists=True,
# )

# print(board_response)

# list_response = trello.create_list(
#     board_id="67754b1a0cf9b3612ab5a37a",
#     list_name="New List",
#     pos="bottom",
# )

# print(list_response)

# card_response = trello.create_card(
#     board_id="67754b1a0cf9b3612ab5a37a",
#     list_name="To Do",
#     card_title="Implement feature X",
#     description="Details about feature X implementation",
# )
# print(card_response)

# move_response = trello.move_card(
#     card_id="67754cb4fa20a4208eaf67e8", list_id="67754bf13fccd9a01d11854c"
# )
# print(move_response)
