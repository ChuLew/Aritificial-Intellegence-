'''
Compute the value brought by a given move by placing a new token for player
at (row, column). The value is the number of opponent pieces getting flipped
by the move.

A move is valid if for the player, the location specified by (row, column) is
(1) empty and (2) will cause some pieces from the other player to flip. The
return value for the function should be the number of pieces hat will be moved.
If the move is not valid, then the value 0 (zero) should be returned. Note
here that row and column both start with index 0.
'''
def get_move_value(state, player, row, column):
	flipped = 0
	# Your implementation goes here
	if(state[row][column]!=' '):
		return 0
	#       up,down,left,right,ul,ur,dl,dr
	rowmv = [-2,2,0,0,-2,-2,2,2]
	colmv = [0,0,-2,2,-2,2,-2,2]
	for i in range(0,len(rowmv)):
		newrow = row + rowmv[i]
		newcol = column + colmv[i]
		if(newrow<0 or newrow>len(state)-1 or
		   newcol<0 or newcol>len(state)-1):
			continue
		midrow = row + rowmv[i]/2
		midcol = column + colmv[i]/2
		opponent = 'W' if player == 'B' else 'B'
		if(state[newrow][newcol]==player and state[midrow][midcol]==opponent):
			flipped+=1
	return flipped

'''
Execute a move that updates the state. A new state should be crated. The move
must be valid. Note that the new state should be a clone of the old state and
in particular, should not share memory with the old state.
'''
def execute_move(state, player, row, column):
	new_state = None
	# Your implementation goes here
	#Make new list for each list in original state and put it in the new_state list
	new_state = [x[:] for x in state]
	rowmv = [-2,2,0,0,-2,-2,2,2]
	colmv = [0,0,-2,2,-2,2,-2,2]
	for i in range(0,len(rowmv)):
		newrow = row + rowmv[i]
		newcol = column + colmv[i]
		if(newrow<0 or newrow>len(state)-1 or
		   newcol<0 or newcol>len(state)-1):
			continue
		midrow = row + rowmv[i]/2
		midcol = column + colmv[i]/2
		opponent = 'W' if player == 'B' else 'B'
		if(state[newrow][newcol]==player and state[midrow][midcol]==opponent):
			new_state[midrow][midcol] = player
	new_state[row][column] = player
	return new_state
'''
A method for counting the pieces owned by the two players for a given state. The
return value should be two tuple in the format of (blackpeices, white pieces), e.g.,

    return (4, 3)

'''
def count_pieces(state):
    blackpieces = 0
    whitepieces = 0
    size= len(state[0])
    for i in range(0,size):
        for j in range(0,size):
            if state[i][j]=="W":
                whitepieces+=1
            if state[i][j]=="B":
                blackpieces+=1
    # Your implementation goes here
    return (blackpieces, whitepieces)

'''
Check whether a state is a terminal state.
'''
def is_terminal_state(state, state_list = None):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] != ' ': continue
            for player in ['B', 'W']:
                if get_move_value(state, player, i, j) > 0:
                    return False

    return True
'''
The minimax algorithm. Your implementation should return the best value for the
given state and player, as well as the next immediate move to take for the player.
'''
import pprint
num_terminal_state = 0
def minimax(state, player):
    global num_terminal_state
    optimal_value = float('-inf') if player == 'B' else float('inf')
    opponent = 'W' if player is 'B' else 'B'

    if is_terminal_state(state):
        num_terminal_state += 1
        bp, wp = count_pieces(state)
        return (bp - wp, -1, -1)

    row = column = -2
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] != ' ': continue
            if get_move_value(state, player, i, j) > 0:
                next_state = execute_move(state, player, i, j)
                next_value, r, c = minimax(next_state, opponent)

                if (r, c) == (-2, -2):
                    next_value, r, c = minimax(next_state, player)

                if (player == 'B' and optimal_value < next_value) or (player == 'W' and optimal_value > next_value):
                    optimal_value = next_value
                    row, column = i, j

    return (optimal_value, row, column)

'''
This method should call the minimax algorithm to compute an optimal move sequence
that leads to an end game.
'''
paths = []
def full_minimax(state, player):
    move_sequence = []

    value, row, col = minimax(state, player)
    state = execute_move(state, player, row, col)
    move_sequence.append((player, row, col))
    turn = 'W' if player == 'B' else 'B'
    optimal_value = max(float('-inf'), value)

    print("Num of Terminal States: %d" % num_terminal_state)

    while (row, col) != (-1, -1):
        value, row, col = minimax(state, turn)
        move_sequence.append((turn, row, col))
        if (row, col) == (-2, -2):
            print("Player %s cannot make a move " % turn)
            move_sequence.pop()
            value = optimal_value

        state = execute_move(state, turn, row, col)
        optimal_value = max(optimal_value, value)
        turn = 'W' if turn == 'B' else 'B'

    pprint.pprint(state)

    return (optimal_value, move_sequence)



'''
The minimax algorithm with alpha-beta pruning. Your implementation should return the
best value for the given state and player, as well as the next immediate move to take
for the player.
'''
def minimax_ab(state, player, alpha = -10000000, beta = 10000000):
	value = 0
	row = -1
	column = -1
	# Your implementation goes here
	if( is_terminal_state(state) ):
		#global term_count
		#term_count+=1
		tup = count_pieces(state)
		paths.append( [(player, row, column)] )
		return (tup[0]-tup[1], row, column)

	moves = []
	for i in range(0,len(state)):
		for j in range(0,len(state)):
			if(get_move_value(state,player,i,j)>0):
				moves.append((i,j))
	if(len(moves)==0):
		if player=='B':
			next_move = minimax_ab(state,'W',alpha,beta)
		elif player=='W':
			next_move = minimax_ab(state,'B',alpha,beta)
		value = next_move[0]
		return (value, row, column)
	value = -10000000 if player=='B' else 10000000

	for mv_tup in moves:
		new_state = execute_move(state,player, mv_tup[0], mv_tup[1])
		#global ab_truncate_count
		if player=='B':
			next_move = minimax_ab(new_state,'W',alpha,beta)
			new_value = max(value, next_move[0])
			#If new value equals beta and it returns, then
			#it means its going from left to right and also ignoring max # of branches possible.
			if not (new_value<beta):
				#ab_truncate_count+=1
				if value!=-10000000:
					paths.pop()
				#so it doesn't early return -10000000 and mess everything up
				value = max(value,new_value)
				return (value,row,column)
			alpha = max(alpha,new_value)
			if new_value>value:
				#replaces old path
				if value!=-10000000:
					paths.pop(len(paths)-2)
				row, column = mv_tup
				value = new_value
			else:
				paths.pop()
		elif player=='W':
			next_move = minimax_ab(new_state,'B',alpha,beta)
			new_value = min(value, next_move[0])
			if not(new_value>alpha):
				#ab_truncate_count+=1
				if value!=10000000:
					paths.pop()
				value = min(value,new_value)
				return (value,row,column)
			beta = min(beta,new_value)
			if new_value<value:
				if value!=10000000:
					paths.pop(len(paths)-2)
				row, column = mv_tup
				value = new_value
			else:
				paths.pop()

	paths[len(paths)-1].append((player, row, column))
	return (value, row, column)

'''
This method should call the minimax_ab algorithm to compute an optimal move sequence
that leads to an end game, using alpha-beta pruning.
'''
def full_minimax_ab(state, player):
	value = 0
	#move_sequence = []
	# Your implementation goes here
	del paths[:]
	tup = minimax_ab(state,player)
	value = tup[0]
	paths[0].reverse()
	#make_report(state)
	return (value, paths[0])
