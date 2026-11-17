import sqlite3 as sql
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = os.environ.get(
    "DB_PATH",
    str(BASE_DIR / "board_games_data.db")
)

dbCon = sql.connect(DB_PATH)
dbCursor = dbCon.cursor()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS board_games_data (
    board_game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_game_name TEXT NOT NULL,
    game_type TEXT,
    game_designer TEXT,
    game_release_date TEXT,
    game_duration INTEGER,
    game_min_players INTEGER,
    game_max_players INTEGER,
    game_age_rating INTEGER
)
""")

dbCon.commit()