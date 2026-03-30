from fastapi import APIRouter, UploadFile, File
import pymupdf
from pathlib import Path
import sqlite3 as sq

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_CURRICULOS = BASE_DIR / "curriculos.db"
DB_PATH_ANALYTICS = BASE_DIR / "analytics.db"

@router.post("/upload/send", tags=["Uploads"])
async def enviar_curriculo(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    data = {
        "filename": file.filename,
        "page_count": len(doc),
        "content": full_text
    }
    
    with sq.connect(str(DB_PATH_CURRICULOS)) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM curriculos")
        cursor.execute("INSERT INTO curriculos (user_id, titulo, conteudo) VALUES (?, ?, ?)", ("default", data["filename"], data["content"]))
    with sq.connect(str(DB_PATH_ANALYTICS)) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM analytics")

    # return analisador_curriculo(data["content"], data["filename"])
    return data