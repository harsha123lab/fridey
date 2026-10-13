"""Persistent SQLite memory and reminder storage."""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DB_PATH = DATA_DIR / "fridey.db"

def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS reminders(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, due_at TEXT, completed INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL);
    """)
    return db

def remember(content: str) -> dict:
    content = content.strip()
    if not content or len(content) > 1000: raise ValueError("Memory must contain 1–1000 characters.")
    with connect() as db:
        db.execute("INSERT OR IGNORE INTO memories(content,created_at) VALUES (?,?)", (content, datetime.now(timezone.utc).isoformat()))
        row = db.execute("SELECT * FROM memories WHERE content=?", (content,)).fetchone()
    return dict(row)

def list_memories() -> list[dict]:
    with connect() as db: return [dict(r) for r in db.execute("SELECT * FROM memories ORDER BY id DESC LIMIT 100")]

def forget(memory_id: int) -> bool:
    with connect() as db: return db.execute("DELETE FROM memories WHERE id=?", (memory_id,)).rowcount > 0

def memory_context(limit: int = 20) -> str:
    items = list_memories()[:limit]
    return "User-approved memories (may be outdated):\n" + "\n".join("- " + x["content"] for x in items) if items else ""

def add_reminder(title: str, due_at: str | None = None) -> dict:
    title = title.strip()
    if not title or len(title) > 500: raise ValueError("Reminder title must contain 1–500 characters.")
    if due_at:
        try: due_at = datetime.fromisoformat(due_at.replace("Z", "+00:00")).isoformat()
        except ValueError as exc: raise ValueError("due_at must be an ISO-8601 date/time.") from exc
    with connect() as db:
        cur = db.execute("INSERT INTO reminders(title,due_at,created_at) VALUES (?,?,?)", (title, due_at, datetime.now(timezone.utc).isoformat()))
        return dict(db.execute("SELECT * FROM reminders WHERE id=?", (cur.lastrowid,)).fetchone())

def list_reminders(include_completed: bool = False) -> list[dict]:
    with connect() as db:
        sql = "SELECT * FROM reminders" + ("" if include_completed else " WHERE completed=0") + " ORDER BY COALESCE(due_at,created_at) LIMIT 200"
        return [dict(r) for r in db.execute(sql)]

def complete_reminder(reminder_id: int) -> bool:
    with connect() as db: return db.execute("UPDATE reminders SET completed=1 WHERE id=?", (reminder_id,)).rowcount > 0

def delete_reminder(reminder_id: int) -> bool:
    with connect() as db: return db.execute("DELETE FROM reminders WHERE id=?", (reminder_id,)).rowcount > 0
