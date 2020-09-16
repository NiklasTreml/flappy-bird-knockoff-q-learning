import flappy_headless
import numpy as np
import sys
from collections import defaultdict
import pickle

rewardAlive = 1
rewardKill = -10000
alpha = 0.1
gamma = 1

Q = defaultdict(lambda:[0,0])  # Q["stateKey"] = (rewardJump, rewardNotJump)
#Q = defaultdict(lambda:(np.random.rand(),np.random.rand()))  # Q["stateKey"] = (rewardJump, rewardNotJump)



#sys.exit()

def paramsToState(params):
    playerVelY = params["playerVelY"]
    playery = params["playery"]
    
    if int(params["upperPipes"][0]["x"]) < 40:
        index = 1
    else:
        index = 0
    
    upperPipex = round(int(params["upperPipes"][index]["x"]) / 5) * 5
    upperPipey = int(params["upperPipes"][index]["y"])

    yDiff = round((playery - upperPipey) / 5) * 5

    state = str(playerVelY) + "_" + \
            str(yDiff) + "_" + \
            str(upperPipex)
    return state

oldState = None
oldAction = None
gameCounter = 0
gameScores = []

def shouldEmulateKeyPress(params):
    global oldState
    global oldAction



    state = paramsToState(params)
    estReward = Q[state]
    prevReward = Q[oldState]

    index = None
    if oldAction:
        index = 1
    else:
        index = 0
    
    prevReward[index] = (1 - alpha) * prevReward[index] + alpha * (rewardAlive + gamma * max(estReward))
    Q[oldState] = prevReward
    oldState = state
    
    
    #print("Estimated Reward: ", estReward)

    if estReward[0] >= estReward[1]:
        #print("Dont jump")
        oldAction = False
        return False
    else:
        #print("Jump")
        oldAction = True
        return True      
    

    


def onGameOver(gameInfo):
    global oldState
    global oldAction
    global gameCounter
    global gameScores

    prevReward = Q[oldState]

    index = None
    if oldAction:
        index = 1
    else:
        index = 0
    
    prevReward[index] = (1 - alpha) * prevReward[index] + alpha * rewardKill
    Q[oldState] = prevReward
    #print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n\n",Q,"\n\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
    
    gameScores.append(gameInfo["score"])
    
    #print("Game Counter: ", gameCounter,"Score:", gameInfo["score"])
    
    if gameCounter % 100 == 0:
        print(str(gameCounter) + ": " + str(np.mean(gameScores[-100:])))
    
    oldState = None
    oldAction = None
    gameCounter += 1

    if gameCounter % 10000 == 0:
        with open("Q\\" + str(gameCounter) + ".pickle", "wb") as file:
            pickle.dump(dict(Q), file)

    


flappy_headless.main(shouldEmulateKeyPress, onGameOver)
