import sqlite3 as sq
from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH_ANALYTICS = BASE_DIR / "analytics.db"

@router.delete("/upload/clear/analytics", tags=["Uploads"])
def deletar_curriculos():
    with sq.connect(str(DB_PATH_ANALYTICS)) as conn:
        # Isso aqui transforma cada linha em algo que aceita acesso por nome de coluna
        conn.row_factory = sq.Row 
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM analytics")
        conn.commit()
        
        return {"message": "Analytics limpos com sucesso!"}