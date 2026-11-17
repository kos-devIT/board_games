import addGames
import readGames
import updateGames 
import deleteGames
import reports

print("Hello board game World")

def mainOptions():
    options = 0
    optionsList = ["1","2","3","4","5","6"]
    userChoises = "Board Games Menu Options\nEnter:\n1. Print.\n2. Add.\n3. Update.\n4. Delete.\n5. Reports.\n6. Exit."
    while options not in optionsList:
        print(userChoises)
        options = input("Enter an option from the board games menu choices above: ")
        if options not in optionsList:
            print(f"{options} is not a valid choice!")
    return options

def reportOptions():
    options = ""
    optionList = ["1","2","3","4"]
    userChoises = "Reports Menu Options\nEnter:\n1. game name.\n2. game type.\n3. game designer.\n4. Exit"
    while options not in optionList:
        print(userChoises)
        options = input("Enter an option from the board games report menu: ")
        if options not in optionList:
            print(f"{options} is not a valid choice!")
    return options



mainProgram = True
while mainProgram:
    mainMenu = mainOptions()
    if mainMenu == "1":
        readGames.read()
    elif mainMenu == "2":
        addGames.addGames()
    elif mainMenu == "3":
        updateGames.update()
    elif mainMenu == "4":
        deleteGames.delete()
    elif mainMenu == "5":
        reportsProgram = True
        while reportsProgram:
            reportsMenu = reportOptions()
            if reportsMenu == "1":
                reports.bgName()
            elif reportsMenu == "2":
                reports.bgType()
            elif reportsMenu == "3":
                reports.bgDesigner()
            else:
                reportsProgram = False
                input(f"Press enter to exit")
    else:
        mainProgram = False
input(f"Press enter to exit, thank you for using the app")