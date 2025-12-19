from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3
from datetime import datetime

api = FastAPI()

# CORS: allow your frontend to call this API
api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", # local testing
        "http://127.0.0.1:5500", # local testing
        "http://localhost:8000", # local testing
        "http://127.0.0.1:8000", # local testing
        "https://gregypo085.github.io", # GitHub Pages
    ],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

DB_PATH = "signups.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS signups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Signup(BaseModel):
    email: EmailStr
    website: str | None = None  # honeypot field

@api.get("/")
def health():
    return {"status": "ok", "message": "GostNode API is running"}

@api.post("/signup")
def signup(data: Signup):
    # Honeypot spam protection
    if data.website:
        raise HTTPException(status_code=400, detail="Invalid submission")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO signups (email, created_at) VALUES (?, ?)",
            (data.email.lower(), datetime.utcnow().isoformat())
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # already exists — silently accept
        pass
    finally:
        conn.close()

    return {"ok": True}

# def index():
#     return {"message": "Hello, Worlds and Greg! VSCode test 3"}

#run fastapi dev main.py
# control + c to stop server