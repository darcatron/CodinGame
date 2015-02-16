w = h = 9
###################################
#### Tests for is_valid_wall ######
###################################
players = [{"x": 0, "y": 0, "wallsLeft": 10}]
me = 0

walls = [{'wallX': 5, 'wallY': 6, 'wallO': 'V'}, 
         {'wallX': 8, 'wallY': 5, 'wallO': 'V'}]
print is_valid_wall(players, me, walls, 4, 4, "V")
print "^should be true^"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {'wallY': 5, 'wallX': 8, 'wallO': 'V'},
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"}]
print is_valid_wall(players, me, walls, 1, 2, "H")
print "^should be false^ for overlay"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {'wallY': 5, 'wallX': 8, 'wallO': 'V'},
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"}]
print is_valid_wall(players, me, walls, 2, 2, "H")
print "^should be false^ for dupe"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {'wallY': 5, 'wallX': 8, 'wallO': 'V'},
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"}]

print is_valid_wall(players, me, walls, 8, 0, "H")
print "^should be false^ for outta bounds"

print is_valid_wall(players, me, walls, 8, 8, "V")
print "^should be false^ for outta bounds"

print is_valid_wall(players, me, walls, 3, 1, "V")
print "^should be false^ for crossing"

print is_valid_wall(players, me, walls, 3, 6, "H")
print "^should be false^ for crossing"

print is_valid_wall(players, me, walls, 3, 7, "H")
print "^should be true^"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"},
         {'wallX': 8, 'wallY': 0, 'wallO': 'V'}, 
         {'wallX': 8, 'wallY': 2, 'wallO': 'V'},
         {"wallX": 8, "wallY": 4, "wallO": "V"}, 
         {"wallX": 8, "wallY": 6, "wallO": "V"},
         {"wallX": 6, "wallY": 8, "wallO": "H"}]

print is_valid_wall(players, me, walls, 6, 7, "V")
print "^should be false^"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"},
         {"wallX": 4, "wallY": 7, "wallO": "V"},
         {"wallX": 4, "wallY": 5, "wallO": "H"},
         {"wallX": 6, "wallY": 3, "wallO": "V"},
         {"wallX": 6, "wallY": 3, "wallO": "H"},
         {"wallX": 8, "wallY": 3, "wallO": "V"},
         {"wallX": 8, "wallY": 0, "wallO": "V"},
         {"wallX": 7, "wallY": 2, "wallO": "H"}]
print is_valid_wall(players, me, walls, 7, 1, "H")
print "^should be false^ for blocking player"

###################################
### Tests for direction_to_gap ####
###################################
players = [{"x": 5, "y": 5, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "RIGHT")
print "^should be UP^ for direction to gap"

players = [{"x": 5, "y": 6, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "RIGHT")
print "^should be UP^ for direction to gap"

players = [{"x": 6, "y": 2, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "RIGHT")
print "^should be DOWN^ for direction to gap"

players = [{"x": 6, "y": 3, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "RIGHT")
print "^should be DOWN^ for direction to gap"



players = [{"x": 6, "y": 5, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "LEFT")
print "^should be UP^ for direction to gap"

players = [{"x": 6, "y": 6, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "LEFT")
print "^should be UP^ for direction to gap"

players = [{"x": 7, "y": 2, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "LEFT")
print "^should be DOWN^ for direction to gap"

players = [{"x": 7, "y": 3, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'}]
print direction_to_gap(walls, players[me], "LEFT")
print "^should be DOWN^ for direction to gap"



players = [{"x": 3, "y": 4, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'},
         {'wallX': 2, 'wallY': 5, 'wallO': 'H'}]
print direction_to_gap(walls, players[me], "DOWN")
print "^should be RIGHT^ for direction to gap"

players = [{"x": 2, "y": 4, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'},
         {'wallX': 2, 'wallY': 5, 'wallO': 'H'}]
print direction_to_gap(walls, players[me], "DOWN")
print "^should be RIGHT^ for direction to gap"

players = [{"x": 5, "y": 6, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'},
         {'wallX': 2, 'wallY': 5, 'wallO': 'H'},
         {'wallX': 4, 'wallY': 7, 'wallO': 'H'}]
print direction_to_gap(walls, players[me], "DOWN")
print "^should be RIGHT^ for direction to gap"

players = [{"x": 5, "y": 6, "wallsLeft": 10}]
walls = [{'wallX': 6, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 7, 'wallY': 2, 'wallO': 'V'},
         {'wallX': 2, 'wallY': 5, 'wallO': 'H'},
         {'wallX': 5, 'wallY': 7, 'wallO': 'H'}]
print direction_to_gap(walls, players[me], "DOWN")
print "^should be LEFT^ for direction to gap"
      
#############################################################################
################# is_possible_to_win restricted case ########################
#############################################################################

players = [{"x": 4, "y": 5, "wallsLeft": 10}]
myId = 0

# Test win is possible with gap up
walls = [{'wallX': 5, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 3, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 3, 'wallO': 'H'},
         {'wallX': 7, 'wallY': 1, 'wallO': 'H'},
         {'wallX': 6, 'wallY': 1, 'wallO': 'H'}]

print is_possible_to_win(players[myId], myId, walls, "UP")
print "^should be true by going through gap up^"


# Test win isn't possible with gap up
walls = [{'wallX': 5, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 5, 'wallO': 'H'},
         {'wallX': 7, 'wallY': 3, 'wallO': 'V'},
         {'wallX': 6, 'wallY': 3, 'wallO': 'H'},
         {'wallX': 8, 'wallY': 1, 'wallO': 'V'},
         {'wallX': 6, 'wallY': 1, 'wallO': 'H'},
         {'wallX': 6, 'wallY': 0, 'wallO': 'V'}]

print is_possible_to_win(players[myId], myId, walls, "UP")
print "^should be false by trying to go through blocked gap up^"


# Test win is possible with gap down
walls = [{'wallX': 5, 'wallY': 4, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 6, 'wallO': 'H'},
         {'wallX': 7, 'wallY': 6, 'wallO': 'V'},
         {'wallX': 6, 'wallY': 8, 'wallO': 'H'}]

print is_possible_to_win(players[myId], myId, walls, "DOWN")
print "^should be true by going through gap down^"

# Test win isn't possible with gap down
walls = [{'wallX': 5, 'wallY': 4, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 6, 'wallO': 'H'},
         {'wallX': 7, 'wallY': 6, 'wallO': 'V'},
         {'wallX': 6, 'wallY': 8, 'wallO': 'H'},
         {'wallX': 8, 'wallY': 7, 'wallO': 'V'}]

print is_possible_to_win(players[myId], myId, walls, "DOWN")
print "^should be false by trying to go through blocked gap down^"

# Simple test isn't possible down
walls = [{'wallX': 5, 'wallY': 4, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 6, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 8, 'wallO': 'H'},
         {'wallX': 7, 'wallY': 7, 'wallO': 'V'}]

print is_possible_to_win(players[myId], myId, walls, "DOWN")
print "^should be false by trying to go through blocked gap down^"

# Simple test is possible down
walls = [{'wallX': 5, 'wallY': 4, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 6, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 8, 'wallO': 'H'}]

print is_possible_to_win(players[myId], myId, walls, "DOWN")
print "^should be true by going through gap down^"


# Simple test win is possible with gap up
walls = [{'wallX': 5, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 3, 'wallO': 'V'}]

print is_possible_to_win(players[myId], myId, walls, "UP")
print "^should be true by going through gap up^"


# Simple test win isn't possible with gap up
walls = [{'wallX': 5, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 3, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 1, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 1, 'wallO': 'H'},
         {'wallX': 7, 'wallY': 0, 'wallO': 'V'}]

print is_possible_to_win(players[myId], myId, walls, "UP")
print "^should be false by trying to go through blocked gap up^"


###################################
# Tests for is_one_move_from_win  #
###################################

# Right before endzone, no wall #
me = 0
players = [{"x": 7, "y": 0, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: RIGHT"

players = [{"x": 7, "y": 3, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: RIGHT"

players = [{"x": 7, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: RIGHT"

me = 1
players = [{}, {"x": 1, "y": 0, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: LEFT"

players = [{}, {"x": 1, "y": 3, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: LEFT"

players = [{}, {"x": 1, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: LEFT"

me = 2
players = [{}, {}, {"x": 0, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 3, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 7, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: DOWN"

# Random areas, no walls #
me = 0
players = [{"x": 6, "y": 0, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: RIGHT"

players = [{"x": 2, "y": 3, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: RIGHT"

players = [{"x": 4, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: RIGHT"

me = 1
players = [{}, {"x": 6, "y": 0, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: LEFT"

players = [{}, {"x": 2, "y": 3, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: LEFT"

players = [{}, {"x": 4, "y": 7, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: LEFT"

me = 2
players = [{}, {}, {"x": 6, "y": 0, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 2, "y": 3, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 4, "y": 6, "wallsLeft": 10}]
walls = []
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: DOWN"


# Last column, walls #
me = 0
players = [{"x": 7, "y": 1, "wallsLeft": 10}]
walls = [{'wallX': 8, 'wallY': 1, 'wallO': 'V'}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: RIGHT"

players = [{"x": 7, "y": 4, "wallsLeft": 10}]
walls = [{'wallX': 8, 'wallY': 1, 'wallO': 'V'},
         {'wallX': 8, 'wallY': 5, 'wallO': 'V'}]
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: RIGHT"

players = [{"x": 7, "y": 8, "wallsLeft": 10}]
walls = [{'wallX': 8, 'wallY': 1, 'wallO': 'V'},
         {'wallX': 8, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 6, 'wallY': 8, 'wallO': 'H'}]
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: RIGHT"

me = 1
players = [{}, {"x": 1, "y": 7, "wallsLeft": 10}]
walls = [{'wallX': 1, 'wallY': 7, 'wallO': 'V'}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: LEFT"

players = [{}, {"x": 1, "y": 4, "wallsLeft": 10}]
walls = [{'wallX': 1, 'wallY': 7, 'wallO': 'V'},
         {'wallX': 1, 'wallY': 5, 'wallO': 'V'}]
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: LEFT"

players = [{}, {"x": 1, "y": 1, "wallsLeft": 10}]
walls = [{'wallX': 1, 'wallY': 7, 'wallO': 'V'},
         {'wallX': 1, 'wallY': 5, 'wallO': 'V'},
         {'wallX': 1, 'wallY': 1, 'wallO': 'H'}]
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: LEFT"

me = 2
players = [{}, {}, {"x": 1, "y": 7, "wallsLeft": 10}]
walls = [{'wallX': 1, 'wallY': 8, 'wallO': 'H'}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 4, "y": 7, "wallsLeft": 10}]
walls = [{'wallX': 1, 'wallY': 8, 'wallO': 'H'},
         {'wallX': 5, 'wallY': 8, 'wallO': 'H'}]
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 7, "y": 7, "wallsLeft": 10}]
walls = [{'wallX': 1, 'wallY': 8, 'wallO': 'V'},
         {'wallX': 5, 'wallY': 8, 'wallO': 'V'},
         {'wallX': 8, 'wallY': 7, 'wallO': 'H'}]
print is_one_move_from_win(players, me, walls)
print "^should be True^ for one move to win endzone: DOWN"

# Random areas, walls #
me = 0
players = [{"x": 4, "y": 4, "wallsLeft": 10}]
walls = [{'wallX': 5, 'wallY': 4, 'wallO': 'V'},
         {'wallX': 4, 'wallY': 2, 'wallO': 'V'},
         {'wallX': 2, 'wallY': 2, 'wallO': 'H'}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: RIGHT"

players = [{"x": 3, "y": 2, "wallsLeft": 10}]
# same walls as before
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: RIGHT"

me = 1
players = [{}, {"x": 4, "y": 4, "wallsLeft": 10}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: LEFT"

players = [{}, {"x": 3, "y": 2, "wallsLeft": 10}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: LEFT"

me = 2
players = [{}, {}, {"x": 4, "y": 4, "wallsLeft": 10}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: DOWN"

players = [{}, {}, {"x": 3, "y": 2, "wallsLeft": 10}]
print is_one_move_from_win(players, me, walls)
print "^should be False^ for one move to win endzone: DOWN"


#######################################
# Tests for direction_towards_player  #
#######################################

