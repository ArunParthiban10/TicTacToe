from copy import deepcopy
from os import system

class Board:
	def __init__(self,other=None):

		self.cells = [[ '_' for i in range(3)] for j in range(3)]

		# Copy constructor
		if other is not None:
			self.cells = deepcopy(other.cells)

	def get_winner(self):
		'''
		returns 'X' if X won, 'O' if O won,'T' if tied,'I' if game is incomplete 
		'''
		cols = []
		# extracts the colums
		for i in range(3):
			cols += [[row[i] for row in self.cells]]

		# extract diagonals 
		digs = [[ self.cells[i][i] for i in range(3)]] + [[ self.cells[i][2-i] for i in range(3)]]

		# check rows
		row_status = self.check_lists(self.cells)

		# check cols
		col_status = self.check_lists(cols)

		# check diag
		dig_status = self.check_lists(digs)
		
		if row_status is not None:
			return row_status

		elif col_status is not None:
			return col_status

		elif dig_status is not None:
			return dig_status
		# If there are no wins in cols,rows and diags
		# If there are emplty spots, game is incomplete
		elif self.get_valid_moves() != []:
			return "I"
		# No empty cells, no winners, so tie
		else:
			return 'T'

	def check_lists(self,lst):
		'''
		Given a 2D this, this function will check is 
		there is a winner, or if X won, ot Y won in that 
		or if the game is incomplete 2D list.

		returns 'X' if X won, 'O' if O won
		'''

		for row in lst:
			
			# Checks is row only contans Xs 
			if 'X' in row and ('O' not in row and '_' not in row):
				return 'X'
			# Checks if row only contains Ys
			elif 'O' in row and ('X' not in row and '_' not in row):
				return 'O'

		return None

	def get_valid_moves(self):
		'''
		Returns a list of the coordinates of the empty spaces 
		in the board
		'''

		# For every cell in cells, if it's empty 
		# then append it to valid_moves
		valid_moves = []
		for row in range(len (self.cells)):
			for cols in range(len(self.cells[0])):
				if self.cells[row][cols] == "_":
					valid_moves.append((row,cols))

		return valid_moves

	def place_move(self, cord, player):
		'''
		Given a tuple(cord) consisting of coordinates
		and a player ('X' or 'O'), this function will
		place the player on that spot.
		'''
		# Create new node, place move, and return it.
		new_node = Board(self)
		new_node.cells[cord[0]][cord[1]] = player
		return new_node


	def minimax(self,player):
		'''
		Standard implementation of the minimax algorithm.
		Computer is X and the user is O. So if Computer wins,
		the score is 1, if the user wins, the score is -1 and 
		if the game is a tie, score is 0. Uses depth first search
		to maximize the computer's gain and minimize the users
		gain
		'''

		# Get the current status of the board
		status = self.get_winner()

		# User won
		if status == 'X':
			return (-1,None)
		# Game is tied
		elif status == 'T':
			return (0,None)
		# Computer one
		elif status == 'O':
			return (1,None) 

		best_score = float('-inf') if player == 'O' else float('inf')

		best_move = None
		# Try every move in valid moves and find the best one
		for move in self.get_valid_moves():
			enemy = 'X' if player=='O' else 'O'
			val = self.place_move(move,player).minimax(enemy)
			
			# If it's computer's turn, try to maximize gains
			if player == 'O':
				if val[0] > best_score :
					best_score = val[0]
					best_move = move 
			# If it's user's turn, try to minimize gains. 
			else:
				if val[0] < best_score :
					best_score = val[0]
					best_move = move 

		return best_score,best_move

	def print_game(self):
		'''
		prints the game
		'''
		print()
		for row in self.cells:
			print(row)
		print()


	def driver(self):
		'''
		The driver funtion that will
		handle gameplay. User starts first
		'''

		system('clear')
		self.print_game()

		# Run until sombody won, or unitl there are free cells
		while self.get_winner()=='I':
			# Get input rom the user and place their moce on the board
			user_move = eval (input("Enter coordinates for X in x,y format: ") )
			self.cells[user_move[0]][user_move[1]] = 'X'

			# Ger move from the computer and place it's move on the board
			computer_move = self.minimax('O')[1]
			if computer_move != None:
				self.cells[computer_move[0]][computer_move[1]] = 'O'

			# Print the new state
			system('clear')
			self.print_game()

			


if __name__ == '__main__':
	game = Board()
	game.driver()















































