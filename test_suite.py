players = [{"x": 0, "y": 0, "wallsLeft": 10}]
me = 0
w = h = 9
###################################
#### Tests for is_valid_wall ######
###################################

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





# Test win is possible with gap down



# Test win isn't possible with gap down
