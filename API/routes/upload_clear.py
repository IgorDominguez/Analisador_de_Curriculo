import sqlite3 as sq
from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_CURRICULOS = BASE_DIR / "curriculos.db"

@router.delete("/upload/clear", tags=["Uploads"])
def deletar_curriculos():
    with sq.connect(str(DB_PATH_CURRICULOS)) as conn:
        # Isso aqui transforma cada linha em algo que aceita acesso por nome de coluna
        conn.row_factory = sq.Row 
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM curriculos")
        conn.commit()
        
        return {"message": "Currículos limpos com sucesso!"}