from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3
from datetime import datetime
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


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

    email = data.email.lower()
    created_at = datetime.utcnow().isoformat()

    # 1 Save to Google Sheet
    try:
        append_email_to_sheet(email, created_at)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Sheets error: {e}")

    # 2 Keeping SQLite for now
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO signups (email, created_at) VALUES (?, ?)",
            (email, created_at)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

    return {"ok": True}


def get_sheets_service():
    service_account_info = json.loads(
        os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    )

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

    service = build("sheets", "v4", credentials=creds)
    return service

def append_email_to_sheet(email: str, created_at: str):
    sheet_id = os.environ["GOOGLE_SHEET_ID"]

    service = get_sheets_service()
    sheet = service.spreadsheets()

    values = [[email, created_at]]

    sheet.values().append(
        spreadsheetId=sheet_id,
        range="A:B",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": values},
    ).execute()


# def index():
#     return {"message": "Hello, Worlds and Greg! VSCode test 3"}

#run fastapi dev main.py
# control + c to stop server