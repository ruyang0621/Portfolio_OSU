self._board = [[Chariot("red"), Elephant("red"), Horse("red"), Guard("red"), 'E', Guard("red"), Elephant("red"), Horse("red"), Chariot("red")],
                       ['E', 'E', 'E', 'E', General("red"), 'E', 'E', 'E', 'E'], 
                       ['E', Cannon("red"), 'E', 'E', 'E', 'E', 'E', Cannon("red"), 'E'],
                       [Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red")],
                       ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
                       [Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue")],
                       ['E', Cannon("blue"), 'E', 'E', 'E', 'E', 'E', Cannon("blue"), 'E'],
                       ['E', 'E', 'E', 'E', General("blue"), 'E', 'E', 'E', 'E'], 
                       [Chariot("blue"), Elephant("blue"), Horse("blue"), Guard("blue"), 'E', Guard("blue"), Elephant("blue"), Horse("blue"), Chariot("blue")]]

self._board = [['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']]

self._board = [[Cannon('blue'), 'E', Elephant('red'), Guard('red'), General('red'), Guard('red'), Chariot('blue'), 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               [Chariot('blue'), 'E', 'E', 'E', Soldier('red'), 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
               ['E', 'E', 'E', 'E', Genral('blue'), 'E', 'E', 'E', 'E'], 
               ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']]

b = board()
j = JanggiGame()
print(j.get_current_player())
print(j.get_game_state())
print(j.get_checked())
print(j.make_move('c7', 'c6'))
print(j.make_move('c1', 'd3'))
print(j.make_move('b10', 'd7'))
print(j.make_move('b3', 'e3'))
print(j.make_move('c10', 'd8'))
print(j.make_move('h1', 'g3'))
print(j.make_move('e7', 'e6'))
print(j.make_move('e3', 'e6'))
print(j.make_move('h8', 'c8'))
print(j.make_move('d3', 'e5'))
print(j.make_move('c8', 'c4'))
print(j.make_move('e5', 'c4'))
print(j.make_move('i10', 'i8'))
print(j.make_move('g4', 'f4'))
print(j.make_move('i8', 'f8'))
print(j.make_move('g3', 'h5'))
print(j.make_move('h10', 'g8'))
print(j.make_move('e6', 'e3'))
print(j.make_move('e9', 'd9'))

b = board()
j = JanggiGame()
print(j.get_current_player())
print(j.get_game_state())
print(j.get_checked())
print(j.make_move('e7', 'e6'))
print(j.make_move('e4', 'e5'))
print(j.make_move('e6', 'e5'))
print(j.make_move('g4', 'f4'))
print(j.make_move('e5', 'e4'))
print(j.make_move('e2', 'd3'))
print(j.make_move('e4', 'f4'))
print(j.make_move('d3', 'e3'))
print(j.make_move('f4', 'e4'))
print(j.make_move('e3', 'f3'))
print(j.make_move('h10', 'g8'))
print(j.make_move('i4', 'h4'))
print(j.make_move('h8', 'f8'))
print(j.make_move('h4', 'g4'))
print(j.make_move('c10', 'd8'))
#checked move self cause check passed
print(j.make_move('g4', 'f4'))
#checked uncheck
print(j.make_move('h3', 'e3'))
#print(j.make_move('e4', 'e3'))
#print(j.make_move('b8', 'e8'))
print(j.make_move('d8', 'e6'))
print(j.make_move('e3', 'e6'))
print(j.make_move('g7', 'f7'))
print(j.make_move('g4', 'f4'))
print(j.make_move('g8', 'h6'))
print(j.make_move('f4', 'g4'))
print(j.make_move('f4', 'f5'))
print(j.make_move('h6', 'g4'))
print(j.make_move('i1', 'i4'))
print(j.make_move('f7', 'f6'))
print(j.make_move('f5', 'f6'))
print(j.make_move('c4', 'c5'))
print(j.make_move('f6', 'e6'))
print(j.make_move('f3', 'e3'))
print(j.make_move('f3', 'f2'))
print(j.make_move('f3', 'f3'))
print(j.make_move('f3', 'e2'))
print(j.make_move('e4', 'e3'))
print(j.make_move('e2', 'e3'))
print(j.make_move('e2', 'f2'))
print(j.make_move('e2', 'e1'))
print(j.make_move('g4', 'e5'))
print(j.make_move('h1', 'i3'))
print(j.make_move('e5', 'f3'))
print(j.make_move('i3', 'g2'))
print(j.make_move('f1', 'e2'))
print(j.make_move('f1', 'f2'))
print(j.make_move('i10', 'h10'))
print(j.make_move('i10', 'h10'))
print(j.make_move('f2', 'f1'))
print(j.make_move('c5', 'd5'))
print(j.make_move('h10', 'h1'))
print(j.make_move('g1', 'g2'))
print(j.make_move('g1', 'd3'))
print(j.make_move('f5', 'g5'))
print(j.make_move('h1', 'g1'))
print(j.get_checked())
print(j.get_game_state())