import json
import sqlite3
import os

DB_FILE = "wallets.db"
print("DB:", os.path.abspath(DB_FILE))
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chain TEXT NOT NULL,
        address TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


init_db()

def get_wallets():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT chain, address FROM wallets")
    wallets = cursor.fetchall()

    conn.close()
    return wallets


def add_wallet(chain, wallet):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO wallets (chain, address) VALUES (?, ?)",
        (chain, wallet),
    )

    conn.commit()
    conn.close()

def remove_wallet(wallet):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM wallets WHERE address = ?",
        (wallet,)
    )

    conn.commit()
    conn.close()