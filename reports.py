from connect import *


def bgName():
    nameField = input("Enter the board game name to search for:  ")
    dbCursor.execute(f"SELECT * FROM board_games_data WHERE board_game_name = '{nameField}' ")
    names = dbCursor.fetchall()
    for name in names:
        print(name)

def bgType():
    typeField = input("Enter the board game type to search for:  ")
    dbCursor.execute(f"SELECT * FROM board_games_data WHERE game_type = '{typeField}' ")
    types = dbCursor.fetchall()
    for type in types:
        print(type)

def bgDesigner():
    designerField = input("Enter the board game designer to search for:  ")
    dbCursor.execute(f"SELECT * FROM board_games_data WHERE game_designer = '{designerField}' ")
    designer = dbCursor.fetchall()
    for design in designer:
        print(design)


if __name__=="__main__":
    bgName()
    bgType()
    bgDesigner()