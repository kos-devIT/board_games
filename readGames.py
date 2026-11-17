from connect import *

def read():
    dbCursor.execute("SELECT * FROM board_games_data")
    bgData = dbCursor.fetchall()
    for i in bgData:
        print(i)

if __name__=="__main__":
    read()