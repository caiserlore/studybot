import sqlite3
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger("Database")

DB_PATH = Path(__file__).parent / "database" / "study.db"

class Database:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(guild_id, user_id, topic)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hypotheses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                thread_id INTEGER,
                number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS labs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                thread_id INTEGER,
                number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS writeups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                thread_id INTEGER,
                number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS counters (
                guild_id INTEGER PRIMARY KEY,
                hypothesis_counter INTEGER DEFAULT 0,
                lab_counter INTEGER DEFAULT 0,
                writeup_counter INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()
        logger.info("Banco de dados inicializado.")

    def mark_completed(self, guild_id: int, user_id: int, topic: str):
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO progress (guild_id, user_id, topic) VALUES (?, ?, ?)",
                (guild_id, user_id, topic)
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao marcar concluído: {e}")
            return False

    def unmark_completed(self, guild_id: int, user_id: int, topic: str):
        self.conn.execute(
            "DELETE FROM progress WHERE guild_id = ? AND user_id = ? AND topic = ?",
            (guild_id, user_id, topic)
        )
        self.conn.commit()

    def is_completed(self, guild_id: int, user_id: int, topic: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM progress WHERE guild_id = ? AND user_id = ? AND topic = ?",
            (guild_id, user_id, topic)
        ).fetchone()
        return row is not None

    def get_user_progress(self, guild_id: int, user_id: int) -> list[str]:
        rows = self.conn.execute(
            "SELECT topic FROM progress WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id)
        ).fetchall()
        return [row["topic"] for row in rows]

    def get_next_counter(self, guild_id: int, counter_type: str) -> int:
        self.conn.execute(
            "INSERT OR IGNORE INTO counters (guild_id) VALUES (?)", (guild_id,)
        )
        row = self.conn.execute(
            f"SELECT {counter_type}_counter FROM counters WHERE guild_id = ?",
            (guild_id,)
        ).fetchone()
        current = row[f"{counter_type}_counter"]
        new_value = current + 1
        self.conn.execute(
            f"UPDATE counters SET {counter_type}_counter = ? WHERE guild_id = ?",
            (new_value, guild_id)
        )
        self.conn.commit()
        return new_value

    def add_note(self, guild_id: int, user_id: int, content: str):
        self.conn.execute(
            "INSERT INTO notes (guild_id, user_id, content) VALUES (?, ?, ?)",
            (guild_id, user_id, content)
        )
        self.conn.commit()

    def search_notes(self, guild_id: int, query: str) -> list:
        rows = self.conn.execute(
            "SELECT * FROM notes WHERE guild_id = ? AND content LIKE ?",
            (guild_id, f"%{query}%")
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self):
        self.conn.close()