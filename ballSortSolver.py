import json, sys, copy, time

blockedSituations = set()

#function that returns all legal moves, given the grid and the current vial
def checkMoves(ballData, current):
    #return empty list if the vial is empty
    if(len(ballData[current]) == 0):
        return list()

    #get the color of the ball we want to move
    color = ballData[current][-1]
    moves = list()

    #check all moves
    i = 0 #index of vial
    for vial in ballData:
        #skip the vial that contains the ball we have to move
        if(current == i):
            i+=1
            continue

        if len(vial) == 0:
            #we don't want to move a ball from a vial we have already completed
            if(not (sameColor(ballData[current]) and len(ballData[current]) == 4)):
                #put the empty vial move at the back, so more meaningful moves can be done before
                moves.append((current, i))
        #if there is a ball of the same color and the vial isn't full
        elif color == vial[-1] and len(vial) < 4:
            moves.insert(0, (current, i))
        
        i+=1

    return moves

#function that checks if a vial contains only balls of the same color
def sameColor(vial):
    if(len(set(vial)) == 1):
        return True
    else:
        return False

#function that checks if the win condition has been met 
def checkWinCon(ballData):
    for vial in ballData:
        #vials must be either empty or have only balls of the same color
        if(vial != []):
            if(len(vial) == 4):
                if(not sameColor(vial)):
                    return False
            else:
                return False
    
    return True

def solve(ballData, current, lastCheck=False):
    if(current == len(ballData)):
        if(lastCheck):
            return False, []
        else:
            current = 0
            lastCheck=True

    if(checkWinCon(ballData)):
        return True, []

    #check possible moves
    moves = checkMoves(ballData, current)

    #if we don't have moves, check next vial
    if(moves == []):
        return solve(ballData, current+1, lastCheck)

    for move in moves:
        ballDataTemp = copy.deepcopy(ballData)
        ball = ballDataTemp[move[0]].pop()
        ballDataTemp[move[1]].append(ball)

        if(makeHash(ballDataTemp) not in blockedSituations):
            blockedSituations.add(makeHash(ballDataTemp))
            
            solved, movesToBeat = solve(ballDataTemp, current, False)
            if(solved):
                movesToBeat.insert(0, move)
                return True, movesToBeat

    return solve(ballData, current+1, lastCheck)
    
#function that makes hash out of the puzzle grid
def makeHash(ballData):
    hashedValue = "|"

    for vial in ballData:
        if(len(vial) > 0):
            for ball in vial:
                hashedValue += str(ball)
            hashedValue += "|"
        else:
            hashedValue += str(0)
            hashedValue += "|"

    return hashedValue

def checkInput(input):
    stdVialLen = len(input[0])
    ballCount = dict()

    for vial in input:
        if(len(vial) != stdVialLen and len(vial) != 0):
            return False
        
        for ball in vial:
            if(ball not in ballCount):
                ballCount[ball] = 0

            ballCount[ball]+=1

    for colour in ballCount:
        if(ballCount[colour] != stdVialLen):
            return False

    return True

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("ERROR: must specify input JSON file!")
        print("Example: python3 ballSortSolver.py puzzle.json")
        exit()
    else:
        jsonFile = open(sys.argv[1],)

    ballDataJson = json.load(jsonFile)
    if(not (checkInput(ballDataJson["puzzle"]))):
        print("Malformed input file!")
        exit()

    ballData = []
    #convert json to list of lists (which will be treated as stacks)
    for row in ballDataJson["puzzle"]:
        ballData.append(row)

    #start from scratch
    startTime = time.time()
    solved, movesToBeat = solve(ballData, 0)
    endTime = time.time()

    if(solved):
        print("Solved!")
        print("Executed in " + str(endTime - startTime) + " seconds")
        print("Solved in " + str(len(movesToBeat)) + " moves")
        for move in movesToBeat:
            print(move)
    else:
        print("Unsolvable!")