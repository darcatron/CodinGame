# TODO 
# 8 Does not take into account heading when counting the number of moves to clear a wall (right now only works for moving right and left)

# NOTES!
# EVERYTHING IS PASSED BY REFERENCE!!!!!!
# LOCKDOWN: force both of us into our forward and therefore his backward which puts us both in the same boat and go shortest path to win!
# if only in lockdown, they can block our exit before we block theirs

# HANDLE
# For lockdown -- Worst Case Scenario: They lock out our exit before we completely lock theirs
# Know when opponent runs out of walls, if they do and we have the shortest path, then we win and there is no need to block with walls
# Oppo starts walling from the start and we can't do lockdown
# build_horizontal_wall_lockdown doesnt work for 3 players
# build_vertical_wall does not take into account if the oppo does not move toward the gap, in the case the oppo moves away from the gap, keep walling oppo

import sys, math, random

########################################################
################ 2 PLAYER STRATEGY #####################
########################################################
def two_players(players, walls, my_id):
    global locked, in_lockdown
    his_id = 1 if my_id == 0 else 0

    if in_lockdown:
        lockdown(players, walls, my_id)
    elif (is_one_move_from_win(players, his_id, walls)): 
        # oppo is about to win!
        # vertical wall them, forcing them towards us, using gap strategy, and blocking their exit
        build_vertical_wall_lockdown(players, his_id, wall_pos, walls)
    else:
        move = best_path()

        if (move == find_opposite_endzone(my_id)): 
            # move makes us go "backwards" 
            in_lockdown = True # make sure it is not a corner case, literally -- whatever that means
            lockdown(players, walls, my_id)
        else:
            print move


def lockdown(players, walls, my_id):
    global locked
    his_id = 1 if my_id == 0 else 0
    force_direction = None
    moves_to_clear = moves_to_clear_wall(walls, players[his_id], "RIGHT" if his_id == 0 else "LEFT")

    if locked:
        pass
    elif (should_lock(players, his_id, walls, myId)): # TODO we must be in the cage with him
        # TODO close his exit
        locked = True
        return
    elif (moves_to_clear == 1):
         build_vertical_wall_lockdown(players, his_id, wall_pos, walls)
    elif (moves_to_clear == 2):
        # TODO This will only trigger for the first horizontal wall, we need something to keep placing h_walls until should_lock is true
        if (force_direction == "UP" and players[his_id]["y"] >= players[myId]["y"]): # oppo is equal or above us
            # build H wall above him
            build_horizontal_wall_lockdown(players, his_id, force_direction, walls)
            return
        elif (force_direction == "DOWN" and players[his_id]["y"] <= players[my_id]["y"]): # oppo is equal or below us
            # build H wall below him
            build_horizontal_wall_lockdown(players, his_id, force_direction, walls)
            return

    print best_path()


########################################################
################ 3 PLAYER STRATEGY #####################
########################################################
def three_players(players, walls, my_id):
    if my_id == 0:
        first_player_of_three(players, walls)
    elif my_id == 1:
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

def is_even(numb):
    return not is_odd(numb)

def is_odd(numb):
    return (numb % 2)

# Checks to see if given position is a corner, returns bool
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
    
    if (position["x"] >= w or position["x"] < 0 or position["y"] >= h or position["y"] < 0):
        return False
    return True


# Returns UP if player_to_be_moved needs to go UP to reach destination_player's row, and
# returns DOWN is player_to_be_moved needs to go DOWN to reach destination_player's row
# If the two players are on the same row, it returns the direction towards the middle of the board
# First arg is generally going to be our position, second his position
def direction_towards_player(destination_player, player_to_be_moved):
    global h

    if destination_player["y"] < player_to_be_moved["y"]:
        return "UP"
    elif destination_player["y"] > player_to_be_moved["y"]:
        return "DOWN"
    else:
        # On same row, so push player_to_be_moved towards middle
        if player_to_be_moved["y"] < (h / 2):
            return "DOWN"
        else:
            return "UP"

    
# Checks if a wall is valid by seeing if another wall is already there or if it goes out of bounds    
def is_valid_wall(players, creator_id, walls, putX, putY, wallO):
    global w, h
    receiver_id = 0 if creator_id == 1 else 1

    if no_walls_left(players[creator_id]) \
        or wall_exists(putX, putY, wallO, walls) \
        or wall_out_of_bounds(putX, putY, wallO, walls) \
        or wall_crosses_or_overlays(putX, putY, wallO, walls) \
        or not is_possible_to_win(players[creator_id], creator_id, walls + [{"wallX": putX, "wallY": putY, "wallO": wallO}])\
        or not is_possible_to_win(players[receiver_id], receiver_id, walls + [{"wallX": putX, "wallY": putY, "wallO": wallO}]):
        return False
    
    # wall is good with the world
    return True

def find_endzone(playerId):
    if playerId == 0:
        return "RIGHT"
    elif playerId == 1:
        return "LEFT"
    elif playerId == 2:
        return "DOWN"

def find_opposite_endzone(playerId):
    if playerId == 0:   
        return "LEFT"
    elif playerId == 1:
        return "RIGHT"
    elif playerId == 2:
        return "UP"

def opposite_direction(direction):
    if direction == "LEFT":
        return "RIGHT"
    elif direction == "RIGHT":
        return "LEFT"
    elif direction == "UP":
        return "DOWN"
    elif direction == "DOWN":
        return "UP" 

def is_one_move_from_win(players, playerId, walls):
    global w, h
    endzone = find_endzone(playerId)

    if (endzone == "RIGHT"):
        if (players[playerId]["x"] == w - 2 and not wall_in_front(walls, players[playerId], endzone)):
            return True
    if (endzone == "LEFT"):
        if (players[playerId]["x"] == 1 and not wall_in_front(walls, players[playerId], endzone)):
            return True
    if (endzone == "DOWN"):
        if (players[playerId]["y"] == h - 2 and not wall_in_front(walls, players[playerId], endzone)):
            return True

    return False            

def no_walls_left(player):
    return player["wallsLeft"] == 0

def wall_exists(putX, putY, wallO, walls):
    return {"wallX": putX, "wallY": putY, "wallO": wallO} in walls

def wall_out_of_bounds(putX, putY, wallO, walls):
    global w, h # grid width and height

    if wallO == "V":
        return (putX >= w) or (putY >= h - 1) or (putX == 0)
    elif wallO == "H":
        return (putX >= w - 1) or (putY >= h) or (putY == 0)
    else:
        print >> sys.stderr, "Err: wall_out_of_bounds got strange orientation"

def wall_crosses_or_overlays(putX, putY, wallO, walls):
    if wallO == "V":
        # wall crosses an existing horizontal wall 
        # or wall would overlay part of existing vertical wall
        return {"wallX": putX - 1, "wallY": putY + 1, "wallO": "H"} in walls \
                or {"wallX": putX, "wallY": putY + 1, "wallO": "V"} in walls
    elif wallO == "H":
        # wall crosses an existing vertical wall 
        # or wall would overlay part of existing horizontal wall
        return {"wallX": putX + 1, "wallY": putY - 1, "wallO": "V"} in walls \
                or {"wallX": putX + 1, "wallY": putY, "wallO": "H"} in walls
    else:
        print >> sys.stderr, "Err: wall_crosses_or_overlays got strange orientation"

#checks if wall is in front of given postion, based on the direction the player intends to move
def wall_in_front(walls, position, heading):
    for wall in walls:
        if heading == "RIGHT":
            if (wall["wallO"] == 'V' and wall["wallX"] == position["x"] + 1 and (wall["wallY"] == position["y"] or wall["wallY"] + 1 == position["y"])):
                return True
        elif heading == "LEFT":
            if (wall["wallO"] == 'V' and wall["wallX"] == position["x"] and (wall["wallY"] == position["y"] or wall["wallY"] + 1 == position["y"])):
                return True
        elif heading == "UP":
            if (wall["wallO"] == 'H' and (wall["wallX"] == position["x"] or wall["wallX"] + 1 == position["x"] ) and wall["wallY"] == position["y"]):
                return True
        elif heading == "DOWN":
            if (wall["wallO"] == 'H' and (wall["wallX"] == position["x"] or wall["wallX"] + 1 == position["x"]) and wall["wallY"] == position["y"] + 1):
                return True
        else:
            print >> sys.stderr, "Invalid heading in wall_in_front"

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


# Wrapper for recursive function win_path_exists
# Determines endzone based on playerId and sets order based on endzone to maximize efficiency based off Sean's guesses
# gap_direction is None for standard call of this function, and is either "UP" or "DOWN" for restricted case
def is_possible_to_win(position, playerId, walls, gap_direction=None):
    global w, h
    # TODO? can use helper func to select endzone
    if playerId == 0:
        endzone = "RIGHT"
        order = ["RIGHT", "UP", "DOWN", "LEFT"]
    elif playerId == 1:
        endzone = "LEFT"
        order = ["LEFT", "UP", "DOWN", "RIGHT"]
    elif playerId == 2:
        endzone = "DOWN"
        order = ["DOWN", "RIGHT", "LEFT", "UP"]

    # Default for regular case
    visited = [[0 for x in range(9)] for y in range(9)]
    

    # check for restricted case
    if gap_direction != None:
        # Depending on the direction of intended travel, mark the column in the opposite direction as visited
        # e.g. if in 3,4 and we intend to go UP then we mark 3,5 & 3,6 & 3,7 & 3,8 as visited
        if gap_direction == "UP" and position["y"] != h - 1:
            # Make all cells below position visited so we don't try for bottom end
            for i in range(position["y"] + 1, h):
                visited[position["x"]][i] = True

        elif gap_direction == "DOWN" and position["y"] != 0:
            # Make all cells above position visited so we don't try for upper end
            for i in range(0, position["y"]):
                visited[position["x"]][i] = True

        else:
            print >> sys.stderr, "gap_direction is weird in is_possible_to_win restricted case!"
    return win_path_exists(walls, position, endzone, order, visited)


# Recursively finds if a path to the endzone exists
def win_path_exists(walls, position, endzone, order, visited):
    global w, h

    # base case
    if endzone == "RIGHT" and position["x"] == w - 1:
        # in endzone, path exists
        return True
    elif endzone == "LEFT" and position["x"] == 0:
        # in endzone, path exists
        return True
    elif endzone == "DOWN" and position["y"] == h -1:
        # in endzone, path exists
        return True

    # flag cell as visited
    visited[position["x"]][position["y"]] = 1

    # Get heading and next_position depending on where the endzone was (order depends on endzone)
    for direction in order:
        if direction == "RIGHT":
            heading = direction
            next_position = {"x": position["x"] + 1, "y": position["y"]}
        elif direction == "UP":
            heading = direction
            next_position = {"x": position["x"], "y": position["y"] - 1}
        elif direction == "DOWN":
            heading = direction
            next_position = {"x": position["x"], "y": position["y"] + 1}
        elif direction == "LEFT":
            heading = direction
            next_position = {"x": position["x"] - 1, "y": position["y"]}

        # Does 3 checks:
            # 1. the next_position is in bounds
            # 2. there's not a wall blocking the way
            # 3. the next_position hasn't been visited yet
        if is_in_bounds(next_position) and not wall_in_front(walls, position, heading) and not visited[next_position["x"]][next_position["y"]]:
            # Recursive case
            if win_path_exists(walls, next_position, endzone, order, visited):
                return True

    return False

# TODO UNTESTED
def best_path(players, playerId, walls):
    if (in_lockdown): # TODO check if fails many times
        # TODO go towards "our" exit, this might be the same as the gap_strategy(). Check it when gap is written
        gap_strategy(players, playerId, walls) # change if this does not work well
    else:
        return gap_strategy(players, playerId, walls)

# TODO UNTESTED
# Sean thinks it is possible that we might have to add is_possible_to_win before every return that hasn't been
# checked yet (or at least most of them)
def gap_strategy(players, playerId, walls):
    endzone = find_endzone(playerId)

    if wall_in_front(walls, players[playerId], endzone):
        dir_to_move = direction_to_gap(walls, players[playerId], endzone)

        if (is_possible_to_win(players[playerId], playerId, walls, dir_to_move): 
            # moving towards gap is a good idea (aka is not a dead end) using restricted is_possible_to_win
            if wall_in_front(walls, players[playerId], dir_to_move):
                return find_opposite_endzone(playerId) # move backwards. This triggers lockdown
            return dir_to_move
        elif wall_in_front(walls, players[playerId], opposite_direction(dir_to_move))):
            return find_opposite_endzone(playerId) # move backwards. This triggers lockdown
        
        # otherwise go other direction
        return opposite_direction(dir_to_move)
    else:
        # move forward towards endzone
        return endzone

# Pre Condition: wall must be in front of position
def direction_to_gap(walls, position, endzone):
    pos_x, pos_y = None, None

    # static starting positions for wall check (x pos for V walls, y pos for H walls)
    if (endzone == "LEFT"):
        pos_x = position['x']
    elif (endzone == "RIGHT"):
        pos_x = position['x'] + 1
    elif (endzone == "DOWN"):
        pos_y = position['y'] + 1

    # based on endzone and cur pos, determine wall starting pos 
    # (y pos for V walls, x pos for H walls)
    if (endzone == "LEFT" or endzone == "RIGHT"):
        if (wall_exists(pos_x, position['y'], 'V', walls)):
            pos_y = position['y']
        elif (wall_exists(pos_x, position['y'] - 1, 'V', walls)):
            pos_y = position['y'] - 1

        if (pos_y == None):
            print >> sys.stderr, "Err: no wall in front of position in direction_to_gap"
        elif (is_even(pos_y)):
             # walls starts on even y pos -> gap is bottom (0 is even)
            return "DOWN"
        return "UP"
    elif (endzone == "DOWN"):
        if (wall_exists(position['x'], pos_y, 'H', walls)):
            pos_x = position['x']
        elif (wall_exists(position['x'] - 1, pos_y, 'H', walls)):
            pos_x = position['x'] - 1 

        if (pos_y == None):
            print >> sys.stderr, "Err: no wall in front of position in direction_to_gap"
        elif (is_even(pos_x)):
            # if walls starts on even x pos -> gap is right (0 is even)
            return "RIGHT"
        return "LEFT"
    else:
        print >> sys.stderr, "Err: Invalid endzone given to direction_to_gap"

def build_horizontal_wall_lockdown(players, receiver_id, wall_pos, walls):
    global lockdown_h_walls

    creator_id = 0 if receiver_id == 1 else 1
    endzone = find_endzone(receiver_id)
    pos_x = players[receiver_id]['x']
    pos_y = players[receiver_id]['y']

    if (endzone == "LEFT"):
        if (wall_pos == "UP"):
            if (is_valid_wall(players, creator_id, walls, pos_x, pos_y, 'H')):
                print pos_x, pos_y, 'H'
                lockdown_h_walls.append({"wallX": pos_x, "wallY": pos_y}) 
            else:
                print >> sys.stderr, "Err: invalid wall -- aka ohhhh shitttt, we got some casses to add in build horizontal wall"
        elif (wall_pos == "DOWN"):
            if (is_valid_wall(players, creator_id, walls, pos_x, pos_y + 1, 'H')):
                print pos_x, pos_y + 1, 'H'
                lockdown_h_walls.append({"wallX": pos_x, "wallY": pos_y + 1})
            else:
                print >> sys.stderr, "Err: invalid wall -- aka ohhhh shitttt, we got some casses to add in build horizontal wall"
    elif (endzone == "RIGHT"):
        if (wall_pos == "UP"):
            if (is_valid_wall(players, creator_id, walls, pos_x - 1, pos_y, 'H')):
                print pos_x - 1, pos_y, 'H'
                lockdown_h_walls.append({"wallX": pos_x - 1, "wallY": pos_y})
            else:
                print >> sys.stderr, "Err: invalid wall -- aka ohhhh shitttt, we got some casses to add in build horizontal wall"
        elif (wall_pos == "DOWN"):
            if (is_valid_wall(players, creator_id, walls, pos_x - 1, pos_y + 1, 'H')):
                print pos_x - 1, pos_y + 1, 'H'
                lockdown_h_walls.append({"wallX": pos_x - 1, "wallY": pos_y + 1})
            else:
                print >> sys.stderr, "Err: invalid wall -- aka ohhhh shitttt, we got some casses to add in build horizontal wall"
    else:
        print >> sys.stderr, "Err: build_horizontal_wall_lockdown was given nonexistant endzone"

# TODO UNTESTED
def build_vertical_wall_lockdown(players, receiver_id, wall_pos, walls):
    # build vertical wall in front of oppo making gap in our direction
    global oppo_gap 
    creator_id = 0 if receiver_id == 1 else 1
    endzone = find_endzone(receiver_id)

    if (not oppo_gap): # determining where gap is for the first and only time
        oppo_gap = direction_towards_player(players[creator_id], players[receiver_id])

    if (oppo_gap == "DOWN"):
        # gap bottom -> build greatest even that is less than or equal to receiver
        check = is_even
    elif (gap == "UP"):
        # gap top -> build greatest odd that is less than or equal to receiver 
        check = is_odd
    else:
        print sys.stderr, "build_vertical_wall_lockdown got a gap that has not yet been implemented"

    if (endzone == "LEFT"):
        if (check(players[receiver_id]['y'])):
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'], players[receiver_id]['y'], 'V')):
                print players[receiver_id]['x'], players[receiver_id]['y'], 'V'
        else: # odd y pos
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'], players[receiver_id]['y'] - 1, 'V')):
                print players[receiver_id]['x'], players[receiver_id]['y'] - 1, 'V'
    elif (endzone == "RIGHT"):
        if (check(players[receiver_id]['y'])):
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'] + 1, players[receiver_id]['y'], 'V')):
                print players[receiver_id]['x'] + 1, players[receiver_id]['y'], 'V'
        else: # odd y pos
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'] + 1, players[receiver_id]['y'] - 1, 'V')):
                print players[receiver_id]['x'] + 1, players[receiver_id]['y'] - 1, 'V'
    else:  
        print sys.stderr, "build_vertical_wall_lockdown got an endzone that has not yet been implemented"


# TODO Untested!
# Helper for should_lock that checks one wall at a time
# Returns +/- 4 for case when we are one horizontal wall from locking, +/- 3 when there is
# a one cell gap, or False otherwise
def should_h_wall_lock(player, h_wall, walls, wall_offset):
    if {"wallX": h_wall["wallX"] + wall_offset, "wallY": h_wall["wallY"] - 1, "wallO": 'V'} in walls:
        # We are one horizontal wall away from the lock
        return wall_offset
    
    if player["y"] >= h_wall["wallY"]:
        # he is on lower side of walls
        if {"wallX": h_wall["wallX"] + wall_offset, "wallY": h_wall["wallY"], "wallO": 'V'} in walls:
            # We are one horizontal wall away from the lock
            return wall_offset
    elif player["y"] < h_wall["wallY"]:
        # he is on upper side of walls
        if {"wallX": h_wall["wallX"] + wall_offset, "wallY": h_wall["wallY"] - 2, "wallO": 'V'} in walls:
            # We are one horizontal wall away from the lock
            return wall_offset
    
    return False


# TODO UNTESTED
# TODO Maybe should return the offset variable so it could return either positive or negative 3 or 4 for the true case
# Returns 4 if we are one horizontal wall from lockdown
# Returns 3 if we currently have a one cell gap between our horizontal wall and the vertical, which
# will require 2 or 3 walls to lock
# Returns False (0) if otherwise
def should_lock(players, his_id, walls, my_id):
    global lockdown_h_walls

    endzone = find_endzone(my_id)

    # Offsets change from positive to negative depending on what direction we are locking in, which
    # is based off our endzone
    if endzone == "RIGHT":
        one_h_wall_offset = 4
        one_cell_gap_offset = 3
    elif endzone == "LEFT":
        one_h_wall_offset = -4
        one_cell_gap_offset = -3

    h_wall = lockdown_h_walls[-1] # get last h_wall placed

    if should_h_wall_lock(players[his_id], h_wall, walls, one_h_wall_offset):
        return 4
    elif should_h_wall_lock(players[his_id], h_wall, walls, one_cell_gap_offset):
        return 3

    return False

# TODO
def lock(players, walls, my_id):
    global lockdown_h_walls, locked

    his_id = 1 if my_id == 0 else 0
    his_endzone = find_endzone(his_id)
    num_away = should_lock(players, his_id, walls, my_id)

    last_h_wall = lockdown_h_walls[-1]

    if num_away == 4:
        # TODO build h wall to lock
        locked = True
    elif num_away == 3:
        # TODO This section is hard. See the three factors that Matush wrote on paper
        if his_endzone == "RIGHT":
            pass
        elif his_endzone == "LEFT":
            pass
        elif his_endzone == "DOWN":
            print >> sys.stderr, "3 players not implemented for lock yet!"
        else:
            print >> sys.stderr, "bad endzone for lock function"

    else:
        print >> sys.stderr, "Bad num_away in lock function"

    locked = True


# TODO
def lock_2_3():
    if wall_exists(last_h_wall["wallX"] + 2, last_h_wall["wallY"] - 1, 'V', walls):
        if is_valid_wall(players, my_id, walls, last_h_wall["wallX"] + 1, last_h_wall["wallY"] - 1, 'H'):
            print last_h_wall["wallX"] + 1, last_h_wall["wallY"] - 1, 'H'
        else:
            print >> sys.stderr, "Invalid wall 3 for right endzone"
    elif is_valid_wall(players, my_id, walls, last_h_wall["wallX"] + 2, last_h_wall["wallY"] - 1, 'V'):
        print last_h_wall["wallX"] + 2, last_h_wall["wallY"] - 1, 'V'
    else:
        print >> sys.stderr, "Invalid wall 2 for right endzone"


# w: width of the board
# h: height of the board
# playerCount: number of players (2 or 3)
# myId: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, playerCount, myId = [int(i) for i in raw_input().split()]
locked, in_lockdown = False, False
lockdown_h_walls = []
oppo_gap = None

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
    
