from connect import *
import readGames

def update():
    gameID = input("Enter the game ID to be updated: ")
    updateField = input("Enter either board_game_name or game_type or game_designer or\ngame_release_date or game_duration or game_min_players or\ngame_max_players or game_age_rating or game_decription to be updated ").title()
    updateValue = input(f"Enter your new data for {updateField}: ")
    updateValue = "'" + updateValue + "'"
    dbCursor.execute(F"UPDATE board_games_data SET {updateField} = {updateValue} WHERE board_game_id = {gameID} ")
    dbCon.commit()
    print(f"Data {gameID} : {updateValue} is updated.")

    readGames.read()

if __name__=="__main__":
    update()
