from agent.agent_chat import send_message
from fastapi import APIRouter
from pathlib import Path
import sqlite3 as sq

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_CHAT = BASE_DIR / "chat.db"

router = APIRouter()

@router.get("/chat/get", tags=["Chat"])
async def coletar_chat():
    with sq.connect(str(DB_PATH_CHAT)) as conn:
        conn.row_factory = sq.Row 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversa")
        rows = cursor.fetchall()

        resultado = [dict(row) for row in rows]

    return {
        "conversa": resultado
    }