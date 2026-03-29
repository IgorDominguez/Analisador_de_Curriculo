from agno.agent import Agent
from agno.models.groq import Groq
from agent.prompts import PROMPT_UPLOADER
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
import re
import sqlite3 as sq
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_MEMORY = BASE_DIR / "memory.db"

load_dotenv()

def create_agent():
    agent = Agent(
        model=Groq(id="openai/gpt-oss-120b"),
        instructions=PROMPT_UPLOADER,
    )

    return agent

def analisador_curriculo(conteudo: str, nome_pdf: str):
    with sq.connect(str(DB_PATH_MEMORY)) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agno_memories")

    agent = create_agent()

    response = agent.run(f"""

    Leia o conteúdo do curriculo abaixo, e armazene as partes mais importantes na sua memória. Lembre-se de organizar as informações de forma que seja fácil de acessar posteriormente, e que não esteja muito grande ou bagunçado. Após isso **retorne o JSON formatado com as informações solicitadas**!

    Currículo:
    {nome_pdf}

    {conteudo}

    """)

    content = response.content.strip()

    if content.startswith("```"):
        content = re.sub(r"```json|```", "", content).strip()

    resposta = json.loads(content)
    # session_id = response.session_id

    # with sq.connect(str(DB_PATH_MEMORY)) as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("DELETE FROM agno_sessions WHERE session_id = ?", (session_id,))

    return resposta