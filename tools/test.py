from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from reddit_tool import RedditTools
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
    tools=[RedditTools(client_id="your_client_id", client_secret="your_client_secret",username="your_username", password="your_password")],
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
post_team.print_response("Create a post on web technologies and frameworks to focus in 2025 on the subreddit r/webdev ", stream=True)