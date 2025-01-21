from phi.agent import Agent
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector



knowledge_base = JSONKnowledgeBase(
    path="agent-toolkit/data",
    vector_db=PgVector(
        table_name="json_docunment_rag",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
)


agent = Agent(
    name="DBAgent",
    knowledge=knowledge_base,
    search_knowledge=True,
    markdown=True,
    instructions=[
        "Use the knowledgebase to provide information.",
        "Search for relevant information in the knowledgebase.",
        "Provide clear and concise responses.",
        "If no information is found, say so.",
    ],
    show_tool_calls=True,
)
agent.knowledge.load(recreate=False)


agent.print_response("Give me names of hackathons happening in 2025 ? ", markdown=True)