import sqlite3 as sq
from pathlib import Path
from fastapi import APIRouter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_MEMORY = BASE_DIR / "memory.db"
DB_PATH_CHAT = BASE_DIR / "chat.db"

router = APIRouter()

@router.delete("/chat/clear", tags=["Chat"])
async def limpar_chat():
    with sq.connect(str(DB_PATH_MEMORY)) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agno_sessions")
        cursor.execute("DELETE FROM agno_memories")
    with sq.connect(str(DB_PATH_CHAT)) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversa")
    return {"message": "Chat limpo com sucesso!"}