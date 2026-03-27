"""
database.py  -  SQLite persistence for cleaned pipeline data.
"""
from pathlib import Path
import sqlite3
import pandas as pd

from logger import get_logger
from pipeline.stage_03_transform import transform

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "app.db"
TABLES = ["inv", "sales", "purch", "exp"]


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS upload_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cur.fetchone() is not None


def _dedupe_table(conn: sqlite3.Connection, table: str) -> None:
    cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if not cols:
        return

    col_list = ", ".join([f'"{c}"' for c in cols])
    conn.execute(
        f"""
        DELETE FROM "{table}"
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM "{table}"
            GROUP BY {col_list}
        )
        """
    )


def merge_context(context: dict, source_filename: str | None = None) -> None:
    with get_connection() as conn:
        for table in TABLES:
            df = context.get(table)
            if df is None or df.empty:
                continue
            df.to_sql(table, conn, if_exists="append", index=False)
            _dedupe_table(conn, table)

        if source_filename:
            conn.execute(
                "INSERT INTO upload_log (filename) VALUES (?)",
                (source_filename,),
            )
        conn.commit()


def load_store() -> dict:
    init_db()

    with get_connection() as conn:
        data = {}
        for table in TABLES:
            if not _table_exists(conn, table):
                data[table] = None
                continue
            df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn)
            data[table] = df if not df.empty else None

    if any(data[t] is None for t in TABLES):
        return {"inv": None, "sales": None, "purch": None, "exp": None, "vars": None, "ready": False}

    context = transform({
        "inv": data["inv"],
        "sales": data["sales"],
        "purch": data["purch"],
        "exp": data["exp"],
    })

    return {
        "inv": data["inv"],
        "sales": data["sales"],
        "purch": data["purch"],
        "exp": data["exp"],
        "vars": context["vars"],
        "ready": True,
    }
