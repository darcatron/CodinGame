players = [{"x": 0, "y": 0, "wallsLeft": 10}]
me = 0
w = h = 9

walls = [{'wallX': 5, 'wallY': 6, 'wallO': 'V'}, 
         {'wallX': 8, 'wallY': 5, 'wallO': 'V'}]
print is_valid_wall(players, me, walls, 4, 4, "V")
print "^should be true^"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {'wallY': 5, 'wallX': 8, 'wallO': 'V'},
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"}]
print is_valid_wall(players, me, walls, 1, 2, "H")
print "^should be false^"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {'wallY': 5, 'wallX': 8, 'wallO': 'V'},
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"}]
print is_valid_wall(players, me, walls, 2, 2, "H")
print "^should be false^"

walls = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
         {'wallY': 5, 'wallX': 8, 'wallO': 'V'},
         {"wallX": 2, "wallY": 2, "wallO": "H"}, 
         {"wallX": 4, "wallY": 5, "wallO": "V"}]

print is_valid_wall(players, me, walls, 8, 0, "H")
print "^should be false^"

print is_valid_wall(players, me, walls, 8, 8, "V")
print "^should be false^"

print is_valid_wall(players, me, walls, 3, 1, "V")
print "^should be false^"

print is_valid_wall(players, me, walls, 3, 6, "H")
print "^should be false^"

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

wallz = [{'wallY': 6, 'wallX': 5, 'wallO': 'V'}, 
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
         