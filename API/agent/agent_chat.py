from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
from pathlib import Path
from agent.prompts import PROMPT_CHAT
from agent.tools.curriculo_get import get_curriculo

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_MEMORY = BASE_DIR / "memory.db"

db = SqliteDb(db_file=str(DB_PATH_MEMORY))

def create_agent():
    agent = Agent(
        model=OpenAIChat(id="gpt-4.1-mini-2025-04-14", temperature=0.3),
        instructions=PROMPT_CHAT,
        db=db,
        add_history_to_context=True,
        num_history_runs=5,
        enable_agentic_memory=True,
        tools=[
            get_curriculo,
        ],
    )

    return agent

def send_message(message):
    agent = create_agent()
    response = agent.run(message)
    return response.content