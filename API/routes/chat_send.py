from agent.agent_chat import send_message
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import sqlite3 as sq

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_CHAT = BASE_DIR / "chat.db"

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.post("/chat/send", tags=["Chat"])
async def chat_send(item: ChatMessage):
    response = send_message(item.message)

    with sq.connect(str(DB_PATH_CHAT)) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversa (user_message, agent_response) VALUES (?, ?)", (item.message, response))

    return {
        "response": response
    }