from connect import *
import readGames

def delete():
    gameID = input("Enter the game ID that you want to be deleted: ")
    dbCursor.execute(F"DELETE FROM board_games_data WHERE board_game_id = {gameID}")
    dbCon.commit()
    print(f"{gameID} is deleted from your database")

    readGames.read()

if __name__=="__main__":
    delete()