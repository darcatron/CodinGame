# TODO 
# 8 Does not take into account heading when counting the number of moves to clear a wall (right now only works for moving right and left)
# TODO
# http://www.codingame.com/replay/33034817

# TODO After alpha testing: (see replays)
#   1. moves_to_clear wall #done (Matush verify)
#   2. check for if they are one from gap ahead of time #done (Matush verify)
#   3. best_path
#   4. Sometimes get to should_lock before placing any horiz walls, which gives list index error
#   5. We missed a check to is_valid_wall (http://www.codingame.com/replay/33628975)
#   6. WHAT THE BALLS (http://www.codingame.com/replay/33630299) and (http://www.codingame.com/replay/33631635) seems like something wrong with vertical wall lockdwon function

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
# TODO maybe. if he goes shortest path instead of gap strategy. Might get through our lockdown through non-gap (I don't think so but you never know)


import sys, math, random

########################################################
################ 2 PLAYER STRATEGY #####################
########################################################
def two_players(players, walls, my_id):
    global in_lockdown
    his_id = 1 if my_id == 0 else 0

    if in_lockdown:
        lockdown(players, walls, my_id)
    # elif we are one move from win
        # move for win
    elif is_one_move_from_win(players, his_id, walls): 
        # oppo is about to win!
        # vertical wall them, forcing them towards us, using gap strategy, and blocking their exit
        build_vertical_wall_lockdown(players, his_id, walls)
    elif one_away_from_gap(players, his_id, walls):
        # if oppo is one away from his gap, then H wall him
        in_lockdown = True
        lockdown(players, walls, my_id)
    else:
        move = best_path(players, my_id, walls)

        if (move == find_opposite_endzone(my_id)): 
            # move makes us go "backwards" 
            in_lockdown = True # make sure it is not a corner case, literally -- whatever that means
            lockdown(players, walls, my_id)
        else:
            print move



def lockdown(players, walls, my_id):
    global locked, horizontal_phase

    his_id = 1 if my_id == 0 else 0
    # force_direction = None  # Sean removed this in favor of using global oppo_gap... objections?
    moves_to_clear = moves_to_clear_wall(walls, players[his_id], "RIGHT" if his_id == 0 else "LEFT")
    print >> sys.stderr, "moves_to_clear == ", moves_to_clear
    if locked:
        if is_one_move_from_win(players, his_id, walls):
            build_vertical_wall_lockdown(players, his_id, walls)
        # else best_path()
    elif (horizontal_phase and should_lock(players, his_id, walls, myId)): # TODO we must be in the cage with him
        # call lock
        lock(players, walls, my_id)
        return
    elif horizontal_phase:
        # check to see he is going to clear horiz wall with upgraded moves_to_clear
        if moves_to_clear_wall(walls, players[his_id], oppo_gap) == 1:
            build_horizontal_wall_lockdown(players, his_id, oppo_gap, walls) # TODO Sean called Matush's functon here, not sure if we built it
                                                                           # it for this case... scary
        else:
            pass # best path()
    elif (moves_to_clear == 1):
         build_vertical_wall_lockdown(players, his_id, walls)
    elif (moves_to_clear == 2):
        print >> sys.stderr, "moves_to_clear == 2"
        if (oppo_gap == "UP" and players[his_id]["y"] <= players[myId]["y"]): # oppo is equal or above us
            # build H wall above him
            build_horizontal_wall_lockdown(players, his_id, oppo_gap, walls)
            horizontal_phase = True
            return
        elif (oppo_gap == "DOWN" and players[his_id]["y"] >= players[my_id]["y"]): # oppo is equal or below us
            # build H wall below him
            build_horizontal_wall_lockdown(players, his_id, oppo_gap, walls)
            horizontal_phase = True
            return

    print >> sys.stderr, "doing best path instead"
    print best_path(players, my_id, walls)


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
    if (position["x"] == 0 or position["x"] == (w - 1)):
        if position["y"] == 0 :
            return True
        elif position["y"] == (h - 1):
            return True
            
    return False
    

def is_in_bounds(position):    
    if (position["x"] >= w or position["x"] < 0 or position["y"] >= h or position["y"] < 0):
        return False
    return True


# Only for two players, works for gap in last column before endzone ONLY
# Tells us if they are going to clear the gap in two moves or not
# TODO Untested
def one_away_from_gap(players, player_id, walls):
    endzone = find_endzone(player_id)
    player_x = players[player_id]["x"]
    player_y = players[player_id]["y"]
    if endzone == "RIGHT":
        col_next_to_endzone = w - 2
        vert_x_offset = 1
        horiz_x_offset = 0
    elif endzone == "LEFT":
        col_next_to_endzone = 1
        vert_x_offset = -1
        horiz_x_offset = -1
    else:
        print >> sys.stderr, "Bad endzone in one_away_from_gap"

    if player_x == col_next_to_endzone:
        if player_y == 1:
            if not wall_exists(player_x + vert_x_offset, player_y - 1, 'V', walls):
                return not wall_exists(player_x + horiz_x_offset, player_y, 'H', walls)
        if player_y == h - 2:
            if not wall_exists(player_x + vert_x_offset, player_y - 1, 'V', walls):
                return not wall_exists(player_x + horiz_x_offset, player_y + 1, 'H', walls)

    return False


# Returns UP if player_to_be_moved needs to go UP to reach destination_player's row, and
# returns DOWN is player_to_be_moved needs to go DOWN to reach destination_player's row
# If the two players are on the same row, it returns the direction towards the middle of the board
# First arg is generally going to be our position, second his position
def direction_towards_player(destination_player, player_to_be_moved):
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
    if wallO == "V":
        return (putX >= w) or (putY >= h - 1) or (putX == 0)
    elif wallO == "H":
        return (putX >= w - 1) or (putY >= h) or (putY == 0)
    else:
        print >> sys.stderr, "Err: wall_out_of_bounds got strange orientation"

# checks if wall passed in will overlay or cross an existing wall
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

#####TODO 8
#### TODO check for later maybe, doesn't take into account other walls in the players
  ## path when trying to circumvent wall_in_front
# Returns 1 if no wall in front
def moves_to_clear_wall(walls, position, heading):
    temp_pos = dict(position)

    if heading == "LEFT" or heading == "RIGHT":
        direction = "y"
    elif heading == "UP" or heading == "DOWN":
        direction = "x"
    else:
        print >> sys.stderr, "Bad heading for moves_to_clear_wall"

    movesUpOrLeft = 1
    movesDownOrRight = 1
    #check num moves to clear by moving up
    while wall_in_front(walls, temp_pos, heading):
        temp_pos[direction] -= 1
        if not is_in_bounds(temp_pos):
            movesUpOrLeft = "inf"
            break
        movesUpOrLeft += 1
    
    temp_pos = dict(position)
    
    #check num moves to clear by moving down
    while wall_in_front(walls, temp_pos, heading):
        temp_pos[direction] += 1
        if not is_in_bounds(temp_pos): # up or left will for sure be less
            print >> sys.stderr, "in moves_to_clear_wall with heading ", heading, " movesUpOrLeft ", movesUpOrLeft, " movesDownOrRight ", movesDownOrRight
            return movesUpOrLeft
        movesDownOrRight += 1

    print >> sys.stderr, "in moves_to_clear_wall with heading ", heading, " movesUpOrLeft ", movesUpOrLeft, " movesDownOrRight ", movesDownOrRight


    return min(movesUpOrLeft, movesDownOrRight)


# Wrapper for recursive function win_path_exists
# Determines endzone based on playerId and sets order based on endzone to maximize efficiency based off Sean's guesses
# gap_direction is None for standard call of this function, and is either "UP" or "DOWN" for restricted case
def is_possible_to_win(position, playerId, walls, gap_direction=None):
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
# TODO fix http://www.codingame.com/replay/33033473 -- OH SHIT
# http://www.codingame.com/replay/33628014
def best_path(players, player_id, walls):
    if (in_lockdown): # TODO check if fails many times
        # TODO go towards "our" exit, this might be the same as the gap_strategy(). Check it when gap is written
        return gap_strategy(players, player_id, walls) # change if this does not work well
    else:
        return gap_strategy(players, player_id, walls)

# TODO
# Sean thinks it is possible that we might have to add is_possible_to_win before every return that hasn't been
# checked yet (or at least most of them)
def gap_strategy(players, player_id, walls):
    cur_goal = goals[-1]

    while ()    

    # endzone = find_endzone(player_id)

    # if wall_in_front(walls, players[player_id], endzone):
    #     dir_to_move = direction_to_gap(walls, players[player_id], endzone)

    #     if (is_possible_to_win(players[player_id], player_id, walls, dir_to_move)): 
    #         # moving towards gap is a good idea (aka is not a dead end) using restricted is_possible_to_win
    #         if wall_in_front(walls, players[player_id], dir_to_move):
    #             return find_opposite_endzone(player_id) # move backwards. This triggers lockdown
    #         return dir_to_move
    #     elif wall_in_front(walls, players[player_id], opposite_direction(dir_to_move)):
    #         return find_opposite_endzone(player_id) # move backwards. This triggers lockdown
        
    #     # otherwise go other direction
    #     return opposite_direction(dir_to_move)
    # else:
    #     # move forward towards endzone
    #     if (is_possible_to_win(players[player_id], player_id, walls, endzone)):
    #         return endzone
    #     else:
    #         print >> sys.stderr, "in gap_strategy, moving towards endzone does not allow for a win"

# TODO
# checks if a coordinate goal is satisfied
def goal_complete():
    pass

# TODO
# checks if a coordinate goal is reachable and does not lead to a dead end
def goal_possible():
    pass


# determines the direction of the gap based on the player's endzone.
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

# builds a horizontal wall above or below the receiver depending on
#  receiver's positon on the grid. The wall_pos is which side of the oppo
#  the wall should be placed and is the same as oppo_gap
def build_horizontal_wall_lockdown(players, receiver_id, wall_pos, walls):
    global lockdown_h_walls

    creator_id = 0 if receiver_id == 1 else 1
    endzone = find_endzone(receiver_id)
    # where to build the wall
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
        print >> sys.stderr, "Err: build_horizontal_wall_lockdown was given nonexistent endzone"

# TODO UNTESTED
# builds a vertical wall above or below the receiver depending on
#  receiver's positon on the grid. The oppo_gap is used to determine 
#  which where the wall should be placed
def build_vertical_wall_lockdown(players, receiver_id, walls):
    # build vertical wall in front of oppo making gap in our direction
    global oppo_gap 
    creator_id = 0 if receiver_id == 1 else 1
    endzone = find_endzone(receiver_id)

    if (not oppo_gap): # determining where gap is for the first and only time
        oppo_gap = direction_towards_player(players[creator_id], players[receiver_id])

    if (oppo_gap == "DOWN"):
        # gap bottom -> build greatest even that is less than or equal to receiver
        check = is_even
    elif (oppo_gap == "UP"):
        # gap top -> build greatest odd that is less than or equal to receiver 
        check = is_odd
    else:
        print >> sys.stderr, "build_vertical_wall_lockdown got a gap that has not yet been implemented"

    if (endzone == "LEFT"):
        if (check(players[receiver_id]['y'])):
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'], players[receiver_id]['y'], 'V')):
                print players[receiver_id]['x'], players[receiver_id]['y'], 'V'
            else:
                print >> sys.stderr, "Err: not a valid V wall in build V wall lockdown endzone == LEFT and check == True"
        else: # odd y pos
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'], players[receiver_id]['y'] - 1, 'V')):
                print players[receiver_id]['x'], players[receiver_id]['y'] - 1, 'V'
            else:
                print >> sys.stderr, "Err: not a valid V wall in build V wall lockdown endzone == LEFT and check == False"
    elif (endzone == "RIGHT"):
        if (check(players[receiver_id]['y'])):
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'] + 1, players[receiver_id]['y'], 'V')):
                print players[receiver_id]['x'] + 1, players[receiver_id]['y'], 'V'
            else:
                print >> sys.stderr, "Err: not a valid V wall in build V wall lockdown endzone == RIGHT and check == True"
        else: # odd y pos
            if (is_valid_wall(players, creator_id, walls, players[receiver_id]['x'] + 1, players[receiver_id]['y'] - 1, 'V')):
                print players[receiver_id]['x'] + 1, players[receiver_id]['y'] - 1, 'V'
            else:
                print >> sys.stderr, "Err: not a valid V wall in build V wall lockdown endzone == RIGHT and check == False"
    else:  
        print >> sys.stderr, "build_vertical_wall_lockdown got an endzone that has not yet been implemented"


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

# TODO if the oppo is near the top or bottom edge, building a wall may close off both paths. We will need to account for
#  this once we test and see how often it happens
def lock(players, walls, my_id):
    global locked

    his_id = 1 if my_id == 0 else 0
    num_away = should_lock(players, his_id, walls, my_id)
    last_h_wall = lockdown_h_walls[-1]
    his_endzone = find_endzone(his_id)
    # where oppo is in relation to H wall (below it or above it)
    his_pos = "DOWN" if players[his_id]['y'] >= last_h_wall['wallY'] else "UP"
    pos_x, pos_y = None, None

    if num_away == 4:
        if (is_valid_wall(players, my_id, walls, last_h_wall["wallX"] + 2, last_h_wall["wallY"], 'H')):
            print last_h_wall["wallX"] + 2, last_h_wall["wallY"], 'H'
            locked = True
        else:
            print >> sys.stderr, "Err: Invalid H wall in lock num_away == 4"
    elif num_away == 3:
        if his_endzone == "RIGHT":
            pos_x = last_h_wall["wallX"] + 3
            pos_y = last_h_wall["wallY"] - 1
        elif his_endzone == "LEFT":
            pos_x = last_h_wall["wallX"] - 1
            pos_y = last_h_wall["wallY"] - 1
        elif his_endzone == "DOWN":
            print >> sys.stderr, "3 players not implemented for lock yet!"
        else:
            print >> sys.stderr, "bad endzone for lock function"

        if (wall_exists(pos_x, pos_y, 'V', walls)):
            lock_2_3(pos_x, pos_y, walls, players, my_id)
        else:
            lock_1_4(players, walls, my_id)

    else:
        print >> sys.stderr, "Bad num_away in lock function"


# TODO UNTESTED
# Begins the 2 - 3 wall build strategy to lock in the oppo.
#  Each call only builds whichever part of the wall is necessary
# See diagram for illustration of wall postions 2 and 3
# Existing wall coordinates are for the vertical wall 
#  necessary to get into lock method 2,3
def lock_2_3(existing_wall_x, existing_wall_y, walls, players, my_id):
    global locked

    his_id = 1 if my_id == 0 else 0
    his_endzone = find_endzone(his_id) 
    last_h_wall = lockdown_h_walls[-1]
    his_pos = "DOWN" if players[his_id]['y'] >= last_h_wall['wallY'] else "UP"
    pos_x_3, pos_y_3, pos_x_2, pos_y_2 = None, None, None, None

    # set wall 2 (x,y) and wall 3 (x)
    if (his_endzone == "LEFT"):
        pos_x_3 = existing_wall_x
        pos_x_2 = existing_wall_x + 1
        pos_y_2 = existing_wall_y
    elif (his_endzone == "RIGHT"):
        pos_x_3 = existing_wall_x - 2
        pos_x_2 = existing_wall_x - 1
        pos_y_2 = existing_wall_y
    else:
        print >> sys.stderr, "Err: Invalid his_endzone in lock_2_3"        

    # set wall 3 (y)
    if (his_pos == "UP"):
        pos_y_3 = existing_wall_y + 2
    elif (his_pos == "DOWN"):
        pos_y_3 = existing_wall_y
    else:
        print >> sys.stderr, "Err: Invalid his_pos in lock_2_3" 

    # if 2 exists
    if(wall_exists(pos_x_2, pos_y_2, 'V', walls)): 
        # build 3
        if (is_valid_wall(pos_x_3, pos_y_3, 'H', walls)):
            print pos_x_3, pos_y_3, 'H'
            locked = True
        else:
            print >> sys.stderr, "Err: Invalid wall 3 in lock_2_3" 

    else:
        # build 2
        if (is_valid_wall(pos_x_2, pos_y_2, 'V', walls)):
            print pos_x_2, pos_y_2, 'V'
        else:
            print >> sys.stderr, "Err: Invalid wall 2 in lock_2_3" 


# TODO UNTESTED
# Begins the 1 - 4 - maybe 6 wall build strategy to lock in the oppo.
#  Each call only builds whichever part of the wall is necessary
# See diagram for illustration of wall postions 1, 4, and 6
def lock_1_4(players, walls, my_id):
    global locked

    his_id = 1 if my_id == 0 else 0
    his_endzone = find_endzone(his_id)
    last_h_wall = lockdown_h_walls[-1]
    his_pos = "DOWN" if players[his_id]['y'] >= last_h_wall['wallY'] else "UP"
    pos_x_1, pos_y_1, pos_x_4, pos_y_4, pos_x_6, pos_y_6 = None, None, None, None

    if (his_endzone == "LEFT"):
        pos_x_1 = last_h_wall["wallX"]
        pos_x_4 = last_h_wall["wallX"] - 1
        pos_x_6 = last_h_wall["wallX"] - 1
    elif (his_endzone == "RIGHT"):
        pos_x_1 = last_h_wall["wallX"] + 2
        pos_x_4 = last_h_wall["wallX"] + 1
        pos_x_6 = last_h_wall["wallX"] + 3
    else:
        print >> sys.stderr, "Err: Invalid his_endzone in lock_1_4"     

    if (his_pos == "UP"):
        pos_y_1 = pos_y_6 = last_h_wall["wallY"]
        pos_y_4 = last_h_wall["wallY"] + 2 
    elif (his_pos == "DOWN"):
        pos_y_1 = pos_y_4 = pos_y_6 = last_h_wall["wallY"] - 2
    else:
         print >> sys.stderr, "Err: Invalid his_pos in lock_1_4"

    # if 1 exists
    if (wall_exists(pos_x_1, pos_y_1, 'V', walls)):
        # if 4 exists 
        if (wall_exists(pos_x_4, pos_y_4, 'H', walls)):
            # if this is reached, we are guaranted 6 is not build since build 4 checks for 6
            if (is_valid_wall(players, my_id, walls, pos_x_6, pos_y_6, 'V')):
                # build 6
                print pos_x_6, pos_y_6, 'V'
                locked = True
            else:
                print >> sys.stderr, "Err: Invalid wall 6 in lock_1_4"
        else:
            # else build 4
            if (is_valid_wall(players, my_id, walls, pos_x_4, pos_y_4, 'H')):
                print pos_x_4, pos_y_4, 'H'
                # check if 6 already exists
                if (wall_exists(pos_x_6, pos_y_6, 'V', walls)):
                    locked = True
            else:
                print >> sys.stderr, "Err: Invalid wall 4 in lock_1_4"
    else:
        # else build 1
        if is_valid_wall(players, my_id, walls, pos_x_1, pos_y_1, 'V'):
            print pos_x_1, pos_y_1, 'V'
        else:
             print >> sys.stderr, "Err: Invalid wall 1 in lock_1_4"


# w: width of the board
# h: height of the board
# playerCount: number of players (2 or 3)
# myId: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, playerCount, myId = [int(i) for i in raw_input().split()]
locked, in_lockdown = False, False
lockdown_h_walls = []
oppo_gap = None
horizontal_phase = False
goals = None
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
        
        if (goals == None):
            goals = [{'x': x, 'y': y}]

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
    
