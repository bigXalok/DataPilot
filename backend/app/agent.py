from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from .database import get_db_schema, engine
from .vector_store import search_vector_store
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

load_dotenv()

# Define the SQL Database
db = SQLDatabase(engine)

@tool
def sql_query_tool(query: str):
    """
    Executes a SQL query against the structured data (CSV uploads).
    Input should be a valid SQLite SQL query.
    """
    return db.run(query)

@tool
def knowledge_retrieval_tool(query: str):
    """
    Retrieves relevant information from uploaded PDFs, reports, and notes.
    Use this for reasoning or context-based questions.
    """
    return search_vector_store(query)

tools = [sql_query_tool, knowledge_retrieval_tool]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are DataPilot, a smart data assistant. 
    You have access to structured data (via SQL) and unstructured knowledge (via retrieval).
    
    CRITICAL INSTRUCTIONS:
    1. If the user asks about "sales", "revenue", or financial performance, search the `knowledge_retrieval_tool` using multiple variations (e.g., "Revenue from operations", "Total Income", "Consolidated Revenue").
    2. The `knowledge_retrieval_tool` is your primary source for annual reports, PDFs, and text documents.
    3. The `sql_query_tool` is ONLY for querying specific CSV or Excel tables you see in the schema below.
    
    Current Database Schema:
    {schema}
    
    If the schema is empty or doesn't have the data, use the retrieval tool. Always explain your reasoning.
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def ask_datapilot(user_input: str, chat_history=None):
    if chat_history is None:
        chat_history = []
    
    schema = get_db_schema()
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history,
        "schema": schema
    })
    return response["output"]
