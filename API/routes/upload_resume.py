from fastapi import APIRouter, UploadFile, File
import pymupdf
from pathlib import Path
from agent.agent_analyser import analisador_curriculo
import sqlite3 as sq

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_CURRICULOS = BASE_DIR / "curriculos.db"

@router.get("/upload/resume", tags=["Uploads"])
async def resumir_curriculo():
    with sq.connect(str(DB_PATH_CURRICULOS)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM curriculos WHERE user_id = ?", ("default",))
        result = cursor.fetchone()

    if result:
        name = result[2]
        content = result[3]
        
        resumo = analisador_curriculo(content, name)

        return resumo
    else:
        return {"error": "Nenhum currículo encontrado para o usuário padrão"}