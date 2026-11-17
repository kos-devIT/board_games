
from connect import *
import readGames

def addGames():
    BGames = []

    bgName = input("Add a board game name: ")
    bgType = input("Add a board game type: ")
    designer = input("Add a board game designer: ")
    relDate = input("Add the release date: ")
    duration = int(input("Add the game duration: "))
    minPlayers = int(input("Add minimum players: "))
    maxPlayers = int(input("Add maximum players: "))
    ageRating = int(input("Add the age rating: "))

    BGames.extend([
        bgName, bgType, designer, relDate,
        duration, minPlayers, maxPlayers, ageRating
    ])

    dbCursor.execute("""
        INSERT INTO board_games_data (
            board_game_name,
            game_type,
            game_designer,
            game_release_date,
            game_duration,
            game_min_players,
            game_max_players,
            game_age_rating
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, BGames)

    dbCon.commit()

    print(f"{bgName} added to the table")

    readGames.read()


if __name__ == "__main__":
    addGames()
