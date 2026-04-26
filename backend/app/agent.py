from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
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

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are DataPilot, a smart data assistant. 
    You have access to structured data (via SQL) and unstructured knowledge (via retrieval).
    
    When a user asks a question:
    1. If it's about numbers, trends, or specific data points in the CSV/SQL tables, use `sql_query_tool`.
    2. If it's about explanations, reasoning, or context from documents, use `knowledge_retrieval_tool`.
    3. If it's a complex question, use BOTH tools and combine the results.
    
    Current Database Schema:
    {schema}
    
    Always explain your reasoning and provide a clear answer. If you use the SQL tool, mention what you found.
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
