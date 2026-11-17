import sqlite3 as sql

dbCon = sql.connect("/home/kos/Coding/projects/board_games/board_games_data.db")
dbCursor = dbCon.cursor()

# ADDED: Create the table if it doesn't exist
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
