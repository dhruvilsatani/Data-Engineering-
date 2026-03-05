import os
import sqlite3
from datetime import datetime

def log(msg: str) -> None:
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}", flush=True)

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def connect_db(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def validate_schema(df, required_cols: set) -> None:
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")