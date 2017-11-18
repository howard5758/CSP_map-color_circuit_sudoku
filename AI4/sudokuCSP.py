# Author: Ping-Jung Liu
# Date: October 14th 2017
# COSC 76 Assignment 4: Constraints Satisfaction Problems
# Acknowledgement: Professor Devin Balkom for providing suggestions 

from CSP import CSP

class sudokuCSP:

	def __init__(self, map):
		# map of sudoku
		self.map = map

	def solve(self):

		X = []
		V = {}
		C = {}

		# all locations are variables
		# locations given number have domain size 1
		for i in range(0, len(self.map)):
			for j in range(0, len(self.map[i])):
				
				X.append((i, j))

				if self.map[i][j] == 0:
					V[(i, j)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
				else:
					V[(i, j)] = [self.map[i][j]]

		# get a list of different integer pairs from 1 to 9
		diff_pair = []
		for i in range(1, 10):
			for j in range(1, 10):
				if not i == j:
					diff_pair.append((i, j))

		# a variable needs to be differnet from its row, column, and 3*3 square
		for i in range(0, len(X)):
			if len(V[X[i]]) == 9:
				for col in range(0, 9):
					if not col == X[i][1]:
						if not (X[i], (X[i][0], col)) in C and not ((X[i][0], col), X[i]) in C:
							C[(X[i], (X[i][0], col))] = diff_pair

				for row in range(0, 9):
					if not row == X[i][0]:
						if not (X[i], (row, X[i][1])) in C and not ((row, X[i][1]), X[i]) in C:
							C[(X[i], (row, X[i][1]))] = diff_pair

				lt = ((X[i][0]//3) * 3, (X[i][1]//3) * 3)

				for c_diff in range(0, 3):
					for r_diff in range(0, 3):
						if not (lt[0] + r_diff, lt[1] + c_diff) == X[i]:
							if not (X[i], (lt[0] + r_diff, lt[1] + c_diff)) in C and not ((lt[0] + r_diff, lt[1] + c_diff), X[i]) in C:
								C[X[i], (lt[0] + r_diff, lt[1] + c_diff)] = diff_pair

		problem = CSP(X, V, C)
		solution = problem.solve()
		
		return solution

	def print_sudoku(self, solution):
		for i in range(0, len(self.map)):
			for j in range(0, len(self.map)):
				print(solution[(i, j)], end='')
			print("")


if __name__ == "__main__":

	sudoku_one = sudokuCSP(((5, 3, 0, 0, 7, 0, 0, 0, 0), (6, 0, 0, 1, 9, 5, 0, 0, 0), (0, 9, 8, 0, 0, 0, 0, 6, 0), (8, 0, 0, 0, 6, 0, 0, 0, 3), (4, 0, 0, 8, 0, 3, 0, 0, 1), (7, 0, 0, 0, 2, 0, 0, 0, 6), (0, 6, 0, 0, 0, 0, 2, 8, 0), (0, 0, 0, 4, 1, 9, 0, 0, 5), (0, 0, 0, 0, 8, 0, 0, 7, 9)))
	sudoku_two = sudokuCSP(((7, 0, 1, 3, 0, 9, 0, 0, 5), (0, 0, 0, 0, 0, 1, 6, 0, 4), (5, 0, 4, 0, 0, 0, 7, 0, 0), (0, 0, 0, 0, 0, 0, 0, 1, 0), (8, 0, 7, 6, 0, 4, 9, 0, 0), (0, 1, 0, 5, 0, 0, 3, 0, 6), (9, 0, 3, 0, 6, 5, 0, 8, 7), (0, 5, 0, 0, 0, 0, 1, 0, 0), (0, 0, 0, 8, 3, 0, 0, 0, 9)))
	
	solution = sudoku_one.solve()
	print("Solution:")
	sudoku_one.print_sudoku(solution)

	solution = sudoku_two.solve()
	print("Solution:")
	sudoku_two.print_sudoku(solution)

