import sqlite3 as sq
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH_CURRICULOS = BASE_DIR / "curriculos.db"

def get_curriculo():
    with sq.connect(str(DB_PATH_CURRICULOS)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT conteudo FROM curriculos")
        resultado = cursor.fetchone()

        return resultado[0] if resultado else None