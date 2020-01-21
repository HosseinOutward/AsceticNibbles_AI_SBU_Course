from Src import GUI, Simulator, AI


def askForAction(x, playerID, arena, gui):
    if x == "IDS":
        return AI.AI_IDS().run(playerID, arena)
    if x == "RBFS":
        return AI.AI_RBFS_S().run(playerID, arena)
    if x == "MINMAX":
        return AI.AI_Alpha_Beta().run(playerID, arena, 15)
    if x == "Q-LEARNING":
        return AI.AI_Q_LEARNING().run(playerID, arena, 20)
    #if x == "A_STAR":
    #    return AI.AI_A_Star().run(playerID, arena)

    return gui.getAction()


def getInit(a):
    if a is "y":
        getInitLoad()

    elif a is "n":
        fScoreAdd = int(input("fScore Add "))
        fScoreMulti = int(input("fScore Multi "))
        width = int(input("Width "))
        height = int(input("Height "))
        consumeMode = input("Consume mode (B or A) ")
        if consumeMode != "B" or "b":
            consumeMode = False
        else:
            consumeMode = True

        numT = int(input("number of teams (one for solo) "))
        numP = int(input("number of players per team"))
        PlayerNames, PlayersType = [], []
        for i in range(numP*numT):
            PlayerNames.append(str(input("name of player from team " + (i%numT+1) + ": ")))
            PlayersType.append(str(input(
                "whats Type of" + PlayerNames[i] + "(type EXACTLY: IDS, MinMax, RBFS, Q-learning (need loading from file) or Human )")).upper())

        winScore = int(input("Score to Win "))
        trnCost = float(input("Turning Penalty "))
        cubeSize = int(input("Window Size (ex. 30 for FHD)"))

        arena = Simulator.Arena(width, height, consumeMode, trnCost, fScoreAdd, fScoreMulti, winScore, numT, PlayerNames, PlayersType)
        gui = GUI.Graphics(width, height, cubeSize, arena)

    else:
        arena = Simulator.Arena(20, 10, True, 0.5, 5, 15, 400, 2, ["1a", "1b", "2a", "2b"], ["MINMAX", "MINMAX", "MINMAX", "MINMAX"])
        gui = GUI.Graphics(20, 10, 30, arena)

    return arena, gui
# ..................................................................


def main():
    #arena, gui = getInit(str(input("Load from file? (y/n) ")))
    arena, gui = getInit(0)

    winner = False
    while not(winner or len(arena.players)==0):
        playerID = 0
        for snake in arena.players:
            gui.drawText("its " + str(snake.name) + " of team " + str(snake.team) + "'s turn", snake.color, 25)
            action = int(askForAction(snake.type, playerID, arena, gui))
            winner = arena.nextTurn(playerID, action)
            gui.redrawPage(arena)
            if winner == 'd':
                winner = False
            else:
                gui.drawText(str(snake.name) + " of team " + str(snake.team) + " score is " + str(arena.getTeamScore(playerID)), snake.color, 1000)
            if winner:
                break
            playerID += 1

    if winner:
        gui.drawText("Winner, Winner, Chicken Dinner. ", (255,215,0), 3000)
        gui.drawText(str(arena.players[playerID].name) + " won.", arena.players[playerID].color, 5000)
    else:
        gui.drawText("GAME OVER", (255,255,255), 1000)
        for snake in arena.players:
            gui.drawText(str(snake.realScore) + " moves by " + str(snake.name), arena.players[playerID].color, 10000)
# ..................................................................


main()
