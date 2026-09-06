# -*- coding: utf-8 -*-
"""
Auth module for Tam Quoc Chi - Chien Luoc.
SQLite-based user management with bcrypt password hashing and JWT tokens.
"""
import sqlite3
import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt as _bcrypt
from jose import JWTError, jwt

# -------------------------------------------------------------------------
# Config
# -------------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "tamquocchi_chienluoc_secret_key_2024_!@#$")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

# Use bcrypt directly (passlib has Python 3.14 compatibility issues)

# -------------------------------------------------------------------------
# Database setup
# -------------------------------------------------------------------------
def get_db():
    """Get SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT UNIQUE NOT NULL,
            email        TEXT UNIQUE NOT NULL,
            password     TEXT NOT NULL,
            display_name TEXT,
            avatar_color TEXT DEFAULT '#f59e0b',
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login   TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_inventory (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
            owned_generals  TEXT NOT NULL DEFAULT '[]',
            owned_tactics   TEXT NOT NULL DEFAULT '[]',
            updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

# -------------------------------------------------------------------------
# Password helpers
# -------------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hash password using bcrypt directly (bypasses passlib Python 3.14 compat issue)."""
    pw_bytes = password.encode('utf-8')[:72]
    return _bcrypt.hashpw(pw_bytes, _bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    pw_bytes = plain.encode('utf-8')[:72]
    return _bcrypt.checkpw(pw_bytes, hashed.encode('utf-8'))


# -------------------------------------------------------------------------
# JWT helpers
# -------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# -------------------------------------------------------------------------
# User CRUD
# -------------------------------------------------------------------------
def create_user(username: str, email: str, password: str, display_name: str = None) -> dict:
    """Create a new user. Returns user dict or raises ValueError."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        # Check uniqueness
        existing = cursor.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()
        if existing:
            raise ValueError("Username hoặc Email đã được sử dụng.")

        hashed = hash_password(password)
        dn = display_name or username
        cursor.execute(
            "INSERT INTO users (username, email, password, display_name) VALUES (?, ?, ?, ?)",
            (username, email, hashed, dn)
        )
        user_id = cursor.lastrowid
        # Create inventory row
        cursor.execute(
            "INSERT INTO user_inventory (user_id, owned_generals, owned_tactics) VALUES (?, '[]', '[]')",
            (user_id,)
        )
        conn.commit()
        return get_user_by_id(user_id)
    finally:
        conn.close()

def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Verify email+password. Returns user dict or None."""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if not row:
            return None
        if not verify_password(password, row["password"]):
            return None
        # Update last_login
        conn.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.now(timezone.utc).isoformat(), row["id"])
        )
        conn.commit()
        return dict(row)
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Optional[dict]:
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_user_safe(user_id: int) -> Optional[dict]:
    """Return user dict without password field."""
    user = get_user_by_id(user_id)
    if user:
        user.pop("password", None)
    return user

# -------------------------------------------------------------------------
# Inventory CRUD
# -------------------------------------------------------------------------
def get_inventory(user_id: int) -> dict:
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT * FROM user_inventory WHERE user_id = ?", (user_id,)
        ).fetchone()
        if not row:
            return {"owned_generals": [], "owned_tactics": []}
        return {
            "owned_generals": json.loads(row["owned_generals"]),
            "owned_tactics": json.loads(row["owned_tactics"]),
            "updated_at": row["updated_at"]
        }
    finally:
        conn.close()

def save_inventory(user_id: int, owned_generals: list, owned_tactics: list) -> dict:
    conn = get_db()
    try:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("""
            INSERT INTO user_inventory (user_id, owned_generals, owned_tactics, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                owned_generals = excluded.owned_generals,
                owned_tactics = excluded.owned_tactics,
                updated_at = excluded.updated_at
        """, (user_id, json.dumps(owned_generals, ensure_ascii=False),
              json.dumps(owned_tactics, ensure_ascii=False), now))
        conn.commit()
        return {"success": True, "updated_at": now}
    finally:
        conn.close()

# Auto-init on import
init_db()
