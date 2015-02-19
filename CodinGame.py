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
from Queue import Queue


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
# UNTESTED
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

# UNTESTED
# TODO fix http://www.codingame.com/replay/33033473 -- OH SHIT
# http://www.codingame.com/replay/33628014
def best_path(players, player_id, walls):
    if (in_lockdown): # TODO check if fails many times
        # TODO go towards "our" exit, this might be the same as the gap_strategy(). Check it when gap is written
        return gap_strategy(players, player_id, walls) # change if this does not work well
    else:
        return gap_strategy(players, player_id, walls)

# UNTESTED
# determines the direction of the gap based on a wall that is blocking the player's path.
def direction_to_gap(walls, wall_in_path, position, heading):
    if heading == "RIGHT" or heading == "LEFT":
        if is_even(wall_in_path["wallY"]):
            return "DOWN"
        return "UP"
    elif heading == "DOWN" or heading == "UP":
        if is_even(wall_in_path["wallX"]):
            return "RIGHT"
        return "LEFT"

    print >> sys.stderr, "Bad heading in direction_to_gap"



# UNTESTED
# No good for three players... for now
def gap_strategy(players, player_id, walls):
    cur_goal = goals[-1]
    endzone = find_endzone(player_id)

    while (goal_complete(players[player_id], cur_goal) or not goal_possible(players[player_id], cur_goal, walls)):
        goals.pop()
        cur_goal = goals[-1]

    if cur_goal['y'] == players[player_id]['y']:
        # goal is in same row as us, find which way
        if cur_goal['x'] < players[player_id]['x']:
            goal_dir = "LEFT"
        else:
            goal_dir = "RIGHT"
        
        # see if there is a wall between us and our goal
        wall_ahead = nearest_vertical_wall_in_row(players[player_id], player_id, walls, cur_goal, goal_dir)

        if (wall_ahead):
            # must overcome the wall, so get gap direction
            gap_direction = direction_to_gap(walls, wall_ahead, players[player_id], goal_dir)
            if (goal_dir == "RIGHT"):
                # Should get to a real gap (a way through after a bunch of walls on top of each other) rather than just get to the top of this one wall
                if (gap_direction == "UP"):
                    goals.append({'x': wall_ahead['wallX'], 'y': wall_ahead['wallY'] - 1})
                elif (gap_direction == "DOWN"):
                    goals.append({'x': wall_ahead['wallX'], 'y': wall_ahead['wallY'] + 2})
            elif (goal_dir == "LEFT"):
                # get gap pretending wall is directly in fronts
                gap_direction = direction_to_gap(walls, wall_ahead, players[player_id], goal_dir)
                if (gap_direction == "UP"):
                    goals.append({'x': wall_ahead['wallX'] - 1, 'y': wall_ahead['wallY'] - 1})
                elif (gap_direction == "DOWN"):
                    goals.append({'x': wall_ahead['wallX'] - 1, 'y': wall_ahead['wallY'] + 2})
        else:
            #TODO no wall ahead to block goal, just move goal_dir, correct?
            pass
    # TODO? elif (we are on same col as goal)
        # Do similar gap strategy but horizontally and not vertically
        # Not sure if we need this, but it could be a good one

    path = shortest_path(players[player_id], cur_goal, walls) # TODO
    # return path[0]
    # matush_path({'x': players[player_id]['x'], 'y': players[player_id]['y']}, cur_goal)
    # path = do_a_star_algo(players[player_id], cur_goal, walls)
    return path[0]


# UNTESTED
# No good for three players
# def get_new_goal(walls, wall_ahead, old_goal_dir, gap_direction):
#     if gap_direction == "UP":
#         while wall_exists(



# UNTESTED
# checks if a coordinate goal is satisfied
def goal_complete(cur_pos, goal):
    if (cur_pos['x'] == goal['x'] and cur_pos['y'] == goal['y']):
        return True

    return False

# UNTESTED
# checks if a coordinate goal is reachable and does not lead to a dead end
 # TODO
def goal_possible(pos, cur_goal, walls):
    # if shortest_path(pos, cur_goal, walls) == False:
    if do_a_star_algo(pos, cur_goal, walls) == False: 
        return False
    return True

# UNTESTED
# Finds nearest vertical wall that blocks advancing in that row
def nearest_vertical_wall_in_row(start_pos, player_id, walls, goal, heading):
    # must account for moving left or moving right depending on heading
    pos_x = start_pos['x']
    pos_y = start_pos['y']


    if (heading == "RIGHT"):
        while (pos_x < goal['x']):
            if (wall_exists(pos_x, pos_y, 'V', walls)):
                return {'wallX': pos_x, 'wallY': pos_y, 'wallO': 'V'}
            elif (wall_exists(pos_x, pos_y - 1, 'V', walls)):
                return {'wallX': pos_x, 'wallY': pos_y - 1, "wallO": 'V'}
            pos_x += 1
    elif (heading == "LEFT"):
        while (pos_x > goal['x']):
            if (wall_exists(pos_x, pos_y, 'V', walls)):
                return {'wallX': pos_x, 'wallY': pos_y, "wallO": 'V'}
            elif (wall_exists(pos_x, pos_y - 1, 'V', walls)):
                return {'wallX': pos_x, 'wallY': pos_y - 1, "wallO": 'V'}
            pos_x -= 1

    return False # no wall


######################## Matush Shortest Path ##############################
## ALL UNTESTED

# Pre-condition: start must be ('x': , 'y': ) only dict
def matush_path(start, goal, walls):
    frontier = Queue()
    frontier.put(start) # TODO send in start as (x,y) dict
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
       current = frontier.get()
       for next in path_neighbors(current, walls):
          if next not in came_from:
             frontier.put(next)
             came_from[next] = current

    reconstruct_path(goal, came_from)

def path_neighbors(pos, walls):
    neighbors = []
    # check left
    if (not wall_in_front(walls, pos, "LEFT")):
        neighbors.append({'x': pos['x'] - 1, 'y': pos['y']})
    # check right
    if (not wall_in_front(walls, pos, "RIGHT")):
        neighbors.append({'x': pos['x'] + 1, 'y': pos['y']})
    # check up
    if (not wall_in_front(walls, pos, "UP")):
        neighbors.append({'x': pos['x'], 'y': pos['y'] - 1})
    # check down
    if (not wall_in_front(walls, pos, "DOWN")):
        neighbors.append({'x': pos['x'], 'y': pos['y'] + 1})

    return neighbors

def reconstruct_path(goal, came_from):
    current = goal 
    path = [current]

    while current != start:
       current = came_from[current]
       path.append(current)

    return path

############################################################################

# UNTESTED
def shortest_path(player_pos, goal, walls):
    global min_so_far
    
    # reset min_so_far to 15
    min_so_far = 15


    if player_pos["x"] == goal["x"] and player_pos["y"] == goal["y"]:
        print >> sys.stderr, "We are at goal. Something bad was passed to shortest_path"
        return False

    # set visited array to all zeroes
    visited = [[0 for x in range(9)] for y in range(9)]

    # set moves to be empty
    moves = []

    long_array = [0] * (w * h + 1) # Guaranteed to have longer length than any possible path


    fewest_moves = calculate_shortest_path(player_pos, goal, walls, visited, moves, long_array)
    if fewest_moves == len(long_array):
        return False
    else:
        return fewest_moves


# Recursive function for shortest_path
# Base case: at goal so return moves_so_far
# Recursive case: not at goal, so try every direction that hasn't been visited and doesn't have a wall in it and is in bounds
# UNTESTED
def calculate_shortest_path(position, goal, walls, visited, moves_so_far, long_array):
    global min_so_far

    # mark as visited
    visited[position["x"]][position["y"]] = 1

    if len(moves_so_far) > min_so_far:
        return moves_so_far

    if position["x"] == goal["x"] and position["y"] == goal["y"]:
        if len(moves_so_far) < min_so_far:
            min_so_far = len(moves_so_far)
        return moves_so_far

    right_pos = {"x": position["x"] + 1, "y": position["y"]}
    up_pos = {"x": position["x"], "y": position["y"] - 1}
    down_pos = {"x": position["x"], "y": position["y"] + 1}
    left_pos = {"x": position["x"] - 1, "y": position["y"]}

    temp_right = list(moves_so_far)
    temp_right.append("RIGHT")
    temp_up = list(moves_so_far)
    temp_up.append("UP")
    temp_down = list(moves_so_far)
    temp_down.append("DOWN")
    temp_left = list(moves_so_far)
    temp_left.append("LEFT")

    visited_temps = [None, None, None, None]

    for i in range(0,4):
        visited_temps[i] = [None] * 9
        for j in range(0,9):
            visited_temps[i][j] = list(visited[j])


    # Does 3 checks:
        # 1. the neighbor is in bounds
        # 2. there's not a wall blocking the way to neighbor
        # 3. the neighbor hasn't been visited yet
    if is_in_bounds(right_pos) and not wall_in_front(walls, position, "RIGHT") and not visited[right_pos["x"]][right_pos["y"]]:
        moves_right = calculate_shortest_path(right_pos, goal, walls, visited_temps[0], temp_right, long_array)
    else:
        moves_right = long_array

    if is_in_bounds(up_pos) and not wall_in_front(walls, position, "UP") and not visited[up_pos["x"]][up_pos["y"]]:
        moves_up = calculate_shortest_path(up_pos, goal, walls, visited_temps[1], temp_up, long_array)
    else:
        moves_up = long_array

    if is_in_bounds(down_pos) and not wall_in_front(walls, position, "DOWN") and not visited[down_pos["x"]][down_pos["y"]]:
        moves_down = calculate_shortest_path(down_pos, goal, walls, visited_temps[2], temp_down, long_array)
    else:
        moves_down = long_array

    if is_in_bounds(left_pos) and not wall_in_front(walls, position, "LEFT") and not visited[left_pos["x"]][left_pos["y"]]:
        moves_left = calculate_shortest_path(left_pos, goal, walls, visited_temps[3], temp_right, long_array)
    else:
        moves_left = long_array

    return get_min_path(moves_right, moves_up, moves_down, moves_left, long_array)


######################## Sean Shortest Path ##############################
## ALL UNTESTED

def distance_from(position, goal):
    return abs(goal["x"] - position["x"]) + abs(goal["y"] - position["y"])

# Goes through position set and finds the position that has the lowest score by indexing
# into the scores array
def get_min_score_pos(position_set, scores):
    min_score_pos = position_set[0]
    min_score = scores[min_score_pos["x"]][min_score_pos["y"]]
    for pos in position_set:
        if scores[pos["x"]][pos["y"]] <= min_score:
            min_score = scores[pos["x"]][pos["y"]]
            min_score_pos = pos

    return min_score_pos


def get_direction(from_pos, to_pos):
    if to_pos["x"] == from_pos["x"] + 1:
        return "RIGHT"
    elif to_pos["x"] == from_pos["x"] - 1:
        return "LEFT"
    elif to_pos["y"] == from_pos["y"] + 1:
        return "DOWN"
    elif to_pos["y"] == from_pos["y"] - 1:
        return "UP"
    else:
        print >> sys.stderr, "Weird positions in get_direction for A* algo"

def reconstruct_path(came_from, current):
    total_path = []
    while current in came_from:
        from_pos = came_from[current["x"]][current["y"]]
        direction = get_direction(from_pos, current)
        total_path.append(direction)
        current = from_pos

    return total_path



# should return a list of positions which is a path to the goal from the start
# will NOT return in terms of RIGHT, UP, DOWN, and LEFT
# TODO doesn't take into account walls yet
# TODO don't let player go through endzone to get to goal?
def do_a_star_algo(position, goal, walls):
    open_set = [dict(position)] # initial node to be evaluated is only start position
    closed_set = []
    came_from = [[None for x in range(9)] for y in range(9)] # initialize empty for all cells in grid
    g_score = [["inf" for x in range(9)] for y in range(9)] # all g_scores are infinity to start
    g_score[position["x"]][position["y"]] = 0 # initialize g_score of start to 0
    f_score = [["inf" for x in range(9)] for y in range(9)] # all f_scores are infinity to start
    f_score[position["x"]][position["y"]] = distance_from(position, goal) # initialize f_score of start to the number of moves to goal without taking into account walls 

    # while there are nodes left to evaluate
    while open_set != []:
        # current node is the one in the open set with lowest f_score value
        current = get_min_score_pos(open_set, f_score)

        # If we reached goal
        if current["x"] == goal["x"] and current["y"] == goal["y"]:
            # reconstruct the path using came_from and return it
            return reconstruct_path(came_from, current)

        # Add it to closed set and remove current from open_set
        closed_set.append(current)
        open_set.remove(current)

        # Get neighbors
        right_pos = {"x": current["x"] + 1, "y": current["y"]}
        up_pos = {"x": current["x"], "y": current["y"] - 1}
        down_pos = {"x": current["x"], "y": current["y"] + 1}
        left_pos = {"x": current["x"] - 1, "y": current["y"]}
        neighbors = [right_pos, up_pos, down_pos, left_pos]

        for neighbor in neighbors:
            # if neighbor is not in closed set
            if not (neighbor in closed_set):
                # tentative_g_score = g_score of current node + 1
                tentative_g_score = g_score[current["x"]][current["y"]] + 1

                # if neighbor not in open_set or tentative_g_score < g_score[neighborX][neighborY]
                if (not (neighbor in open_set)) or (tentative_g_score < g_score[neighbor["x"]][neighbor["y"]]):
                    # came_from[neighborX][neighborY] = current node (something like: {'x': 4, 'y': 4})
                    came_from[neighbor["x"]][neighbor["y"]] = current # TODO May have to make a copy of current here
                    g_score[neighbor["x"]][neighbor["y"]] = tentative_g_score
                    f_score[neighbor["x"]][neighbor["y"]] = g_score[neighbor["x"]][neighbor["y"]] + distance_from(neighbor, goal)
                    # if neighbor not in open_set
                    if not (neighbor in open_set):
                        # add neighbor to open_set
                        open_set.append(neighbor)

    # No path found
    return False



def get_min_path(moves_right, moves_up, moves_down, moves_left, long_array):
    min_moves = min(len(moves_right), len(moves_up), len(moves_down), len(moves_left))
    if min_moves == len(moves_right):
        return moves_right #.insert(0, "RIGHT") # TODO (get rid of this if other thing works) prepend RIGHT to list of moves since you know that is the way to the shortest path from here
    elif min_moves == len(moves_up):
        return moves_up
    elif min_moves == len(moves_down):
        return moves_down
    elif min_moves == len(moves_left):
        return moves_left
    elif min_moves == len(long_array):
        # All of the neighbors failed
        return long_array
    else:
        print >> sys.stderr, "Bad min_moves in get_min_path"
###########################################################################

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

# UNTESTED
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


# Untested!
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


# UNTESTED
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


# UNTESTED
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


# UNTESTED
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
min_so_far = 15

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
        
        if (goals == None and player == myId):
            goals = [{'x': w - 1, 'y': y}]

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
    
