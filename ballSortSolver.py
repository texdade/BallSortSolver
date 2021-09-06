import json, sys, copy

#define pass_by_value decorator
def pass_by_value(f):
    def _f(*args, **kwargs):
        args_copied = copy.deepcopy(args)
        kwargs_copied = copy.deepcopy(kwargs)
        return f(*args_copied, **kwargs_copied)
    return _f

def checkMoves(ballData, blockedMoves, current):
    #return empty list if the vial is empty
    if(len(ballData[current]) == 0):
        return []

    #get the color of the ball when want to move
    color = ballData[current][-1]
    moves = set()

    #check all moves
    i = 0 #index of vial
    for vial in ballData:
        #skip the vial that contains the ball we have to move
        if(current == i):
            i+=1
            continue

        #if not blocked, an empty vial is always a move
        if len(vial) == 0:
            if not (current, i) in blockedMoves:
                moves.add((current, i))
        #if there is a ball of the same color and the vial isn't full
        elif color == vial[-1] and len(vial) < 4:
            #check if the move isn't blocked
            if not (current, i) in blockedMoves:
                moves.add((current, i))
        
        i+=1
    
    return moves

def checkWinCon(ballData):
    for vial in ballData:
        #vials must be either empty or have only balls of the same color
        if(vial != []):
            color = vial[0]
            for ball in vial:
                if ball != color:
                    return False
    
    return True

@pass_by_value
def solve(ballData, blockedMoves, current, fromVial, toVial):
    print(ballData)

    if(fromVial != -1 and toVial != -1):
        ball = ballData[fromVial].pop()
        ballData[toVial].append(ball)
        blockedMoves.add((toVial, fromVial))

    checkWinCon(ballData)

    #check possible moves
    moves = checkMoves(ballData, blockedMoves, current)

    #if we don't have moves, check next vial
    if(moves == []):
        if(solve(ballData, blockedMoves, current+1, -1, -1)):
            return True

    for move in moves:
        if(solve(ballData, blockedMoves, current, move[0], move[1])):
            return True


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("ERROR: must specify input JSON file!")
        print("Example: python3 ballSortSolver.py puzzle.json")
        exit()
    else:
        jsonFile = open(sys.argv[1],)

    ballDataJson = json.load(jsonFile)

    ballData = []
    #convert json to list of lists (which will be treated as stacks)
    for row in ballDataJson["puzzle"]:
        ballData.append(row)

    #start from scratch
    solved = solve(ballData, set(), 0, -1, -1)

    if(solved):
        print("Solved!")
    else:
        print("Unsolvable!")