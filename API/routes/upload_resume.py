from fastapi import APIRouter, UploadFile, File
import pymupdf
from pathlib import Path
from agent.agent_analyser import analisador_curriculo
import sqlite3 as sq

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_CURRICULOS = BASE_DIR / "curriculos.db"
DB_PATH_ANALYTICS = BASE_DIR / "analytics.db"

@router.get("/upload/resume", tags=["Uploads"])
async def resumir_curriculo():
    with sq.connect(str(DB_PATH_CURRICULOS)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM curriculos WHERE user_id = ?", ("default",))
        result = cursor.fetchone()

    if result:
        user_id = "default"
        name = result[2]
        content = result[3]
        
        resumo = analisador_curriculo(content, name)

        with sq.connect(str(DB_PATH_ANALYTICS)) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analytics WHERE user_id = ?", (user_id,))
            cursor.execute("INSERT INTO analytics (user_id, participante, idade, linkedin, github, resumo) VALUES (?, ?, ?, ?, ?, ?)", (user_id, resumo["nome"], resumo["idade"], resumo["linkedin"], resumo["github"], resumo["resumo"]))
            conn.commit()

        return resumo
    else:
        return {"error": "Nenhum currículo encontrado para o usuário padrão"}