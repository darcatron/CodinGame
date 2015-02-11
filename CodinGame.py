# TODO 
# 4 IF THE WALL IS WITHIN BOUNDS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 5 IF THE WALL BLOCKS OFF A PLAYERS PATH
# 6 IF THE WALL OVERLAYS PART OF ANOTHER WALL
# 8 Does not take into account heading when counting the number of moves to clear a wall (right now only works for moving right and left)

# NOTES!
#EVERYTHING IS PASSED BY REFERENCE!!!!!!
# LOCKDOWN: force both of us into our forward and therefore his backward which puts us both in the same boat and go shortest path to win!

# HANDLE
# For lockdown -- Worst Case Scenario: They lock out our exit before we completely lock theirs
# Know when opponent runs out of walls, if they do and we have the shortest path, then we win and there is no need to block with walls

import sys, math, random

########################################################
################ 2 PLAYER STRATEGY #####################
########################################################
def two_players(players, walls, myId):
    if myId == 0:
        first_player_of_two(players, walls)
    else:
        second_player_of_two(players, walls)


#Strategy for two players if we move first
def first_player_of_two(players, walls):
    myId = 0
    hisId = 1
    #if he is in corner, wall him
    if is_corner(players[hisId]):
        if players[hisId]["y"] == 0:
            putY = 0
        else:
            putY = players[hisId]["y"] - 1
        putX = w - 1
        
        if is_valid_wall(players, myId, walls, putX, putY, "V"):
            print putX, putY, "V"
        else:
            print >> sys.stderr, "Wall not valid in corner! FIX IT"
    
    #TODO 1
    else:
        #if wall to our right
        if wall_in_front(walls, players[myId], "RIGHT"):
            #TODO 2 
            results = moves_to_clear_wall(walls, players[myId], "RIGHT")
            movesToClearWall = results[0]
            bestDirection = results[1]
            if (movesToClearWall > 1):
                #TODO 3
                print random.randrange(1,9), random.randrange(0,9), "V"
            else:
                #clear the wall
                print bestDirection
        else:
            print "RIGHT"
        

#Strategy for two players if we move second
def second_player_of_two(players, walls):
    myId = 1
    pass
    

########################################################
################ 3 PLAYER STRATEGY #####################
########################################################
def three_players(players, walls, myId):
    if myId == 0:
        first_player_of_three(players, walls)
    elif myId == 1:
        second_player_of_three(players, walls)
    else:
        third_player_of_three(players, walls)

#Strategy for three players if we move first
def first_player_of_three(players, walls):
    myId = 0
    pass

#Strategy for three players if we move second
def second_player_of_three(players, walls):
    myId = 1
    pass

#Strategy for three players if we move third
def third_player_of_three(players, walls):
    myId = 2
    pass


#######################################################
################ HELPER FUNCTIONS #####################
#######################################################

#Checks to see if given position is a corner, returns bool
def is_corner(position):
    global w, h
    
    if (position["x"] == 0 or position["x"] == (w - 1)):
        if position["y"] == 0 :
            return True
        elif position["y"] == (h - 1):
            return True
            
    return False
    

def is_in_bounds(position):
    global w, h
    
    if (position["x"] >= w or position["y"] >= h):
        return False
    return True
    
#Checks if a wall is valid by seeing if another wall is already there or if it goes out of bounds    
def is_valid_wall(players, myId, walls, putX, putY, wallO):
    #TODO 4, 5, 6
    global w, h

    if players[myId]["wallsLeft"] == 0: 
        # no walls left
        return False
    elif {"wallX": putX, "wallY": putY, "wallO": wallO} in walls:
        # wall already exists
        return False
    elif wallO == "V":
        if {"wallX": putX - 1, "wallY": putY + 1, "wallO": "H"} in walls:
            # wall crosses an existing horizontal wall
            return False
        if putX >= w or (putY >= h - 1) or putX == 0:
            #wall is out of bounds
            return False
    elif wallO == "H":
        if {"wallX": putX + 1, "wallY": putY - 1, "wallO": "V"} in walls:
            # wall crosses an existing vertical wall
            return False
        if (putX >= w - 1) or putY >= h or putY == 0:
            #wall is out of bounds
            return False
    
    return True


#checks if wall is in front of given postion, based on the direction the player is heading
def wall_in_front(walls, position, heading):
    for wall in walls:
        if heading == "RIGHT":
            if (wall["wallO"] == 'V' and wall["wallX"] == position["x"] + 1 and (wall["wallY"] == position["y"] or wall["wallY"] + 1 == position["y"])):
                return True
        elif heading == "LEFT":
            if (wall["wallO"] == 'V' and wall["wallX"] == position["x"] - 1 and (wall["wallY"] == position["y"] or wall["wallY"] + 1 == position["y"])):
                return True

    return False


def moves_to_clear_wall(walls, position, heading):
    originalPos = dict(position)
    movesUp = 0
    movesDown = 0
    
    #####TODO 8
    
    #check num moves to clear by moving up
    while wall_in_front(walls, originalPos, heading):
        originalPos["y"] -= 1
        if not is_in_bounds(originalPos):
            movesUp = "inf"
            break
        movesUp += 1
    
    originalPos = dict(position)
    
    #check num moves to clear by moving down
    while wall_in_front(walls, originalPos, heading):
        originalPos["y"] += 1
        if not is_in_bounds(originalPos):
            return [movesUp, "UP"]
        movesDown += 1
    if (min(movesUp, movesDown) == movesDown):
        return [movesDown, "DOWN"]
    else:
        return [movesUp, "UP"]




# w: width of the board
# h: height of the board
# playerCount: number of players (2 or 3)
# myId: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, playerCount, myId = [int(i) for i in raw_input().split()]

# game loop
while 1:
    players = []
    walls = []
    for player in range(playerCount):
        # x: x-coordinate of the player
        # y: y-coordinate of the player
        # wallsLeft: number of walls available for the player
        x, y, wallsLeft = [int(i) for i in raw_input().split()]
        players.append({"x": x,"y": y, "wallsLeft" : wallsLeft})
    wallCount = int(raw_input()) # number of walls on the board
    for i in xrange(wallCount):
        # wallX: x-coordinate of the wall
        # wallY: y-coordinate of the wall
        # wallOrientation: wall orientation ('H' or 'V')
        wallX, wallY, wallOrientation = raw_input().split()
        wallX = int(wallX)
        wallY = int(wallY)
        walls.append({"wallX" : wallX, "wallY" : wallY, "wallO" : wallOrientation})

        
    if playerCount == 2:
        two_players(players, walls, myId)
    else:
        three_players(players, walls, myId)
        
        
        # print >> sys.stderr, "wallX, wallY", wallX, wallY
        # wall in front of me
        # only plays defensively left to right
        # if (wallOrientation == 'V' and wallX == my_pos[0] + 1 and (wallY == my_pos[1] or wallY + 1 == my_pos[1])):
        #     if (my_pos[1] == 0):
        #         to_print = "DOWN"
        #     elif (my_pos[1] == w - 1):
        #         to_print = "UP"
        #     elif (wallY == my_pos[1]):
        #         to_print = "UP"
        #     elif (wallY + 1 == my_pos[1]):
        #         to_print = "DOWN"
        
    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall    
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    
