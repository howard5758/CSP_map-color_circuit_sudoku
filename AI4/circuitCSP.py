# Author: Ping-Jung Liu
# Date: October 14th 2017
# COSC 76 Assignment 4: Constraints Satisfaction Problems
# Acknowledgement: Professor Devin Balkom for providing suggestions 

from CSP import CSP

class circuitCSP:

	def __init__(self, bt_mc, width, height, Components):
		# width and height of board
		self.height = height
		self.width = width
		# list of components widths and heights
		self.Components = Components
		# 1 --> solve with backtracking   0 --> solve with min_conflict
		self.bt_mc = bt_mc

	def solve(self):

		X = []
		V = {}
		C = {}

		# initialize variable and domain
		for i in range(0, len(self.Components)):
			X.append(i)
			component_width = self.Components[i][0]
			component_height = self.Components[i][1]

			# possible lower left point of a component
			for x in range(0, self.width):
				for y in range(0, self.height):
					# if legal, append to V
					if x + component_width <= self.width and y + component_height <= self.height:
						if i in V:
							V[i].append((x, y))
						else:
							V[i] = [(x, y)]
		
		# initialize constraints
		for i in range(0, len(X)):
			for j in range(0, len(X)):
				if not i == j:
					if not (i, j) in C and not (j, i) in C:
						C[(i, j)] = self.get_cons(i, j, V)

		#print(X)
		#print(V)
		#print(C)

		problem = CSP(X, V, C)

		# solve
		if self.bt_mc == 1:
			solution = problem.solve()
		else:
			solution = problem.min_conflicts(1000)
		result = {}
	
		if solution == None:
			return None

		for idx in solution:
			result[tuple(self.Components[idx])] = solution[idx]

		return result

	# get the constraint lists for variable i and j
	def get_cons(self, i, j, V):
		width = self.width
		height = self.height
		c = []

		for vi in V[i]:
			for vj in V[j]:

				i_lb = vi
				i_ru = (vi[0] + self.Components[i][0] - 1, vi[1] + self.Components[i][1] - 1)
				j_lb = vj
				j_ru = (vj[0] + self.Components[j][0] - 1, vj[1] + self.Components[j][1] - 1)

				if i_lb[0] > j_ru[0] or j_lb[0] > i_ru[0] or i_ru[1] < j_lb[1] or j_ru[1] < i_lb[1]:
					c.append((vi, vj))

		return c

	# print the circuit
	def print_circuit(self, solution):
		if solution == None:
			print("No Solution")
		else:
			for j in range(0, self.height):
				for i in range(0, self.width):
					p = False
					for component in solution:
						if i >= solution[component][0] and i < solution[component][0] + component[0] and (self.height - j - 1) >= solution[component][1] and (self.height - j - 1) < solution[component][1] + component[1]:	
							print(self.Components.index(component), end='')
							p = True
							break
					if not p:
						print("#", end='')
				print("")

if __name__ == "__main__":

	#new_circuit = circuitCSP(1, 10, 5, [(3, 2), (5, 2), (2, 3), (4, 1), (2, 1), (1, 1)])
	new_circuit = circuitCSP(0, 10, 10, [(4, 4), (5, 5), (3, 3), (2, 4), (4, 2), (6, 1), (4, 1), (1, 9), (2, 5), (2, 2)])
	#new_circuit = circuitCSP(1, 10, 3, [(3, 2), (5, 2), (7, 1), (2, 3)])
	#new_circuit = circuitCSP(1, 5, 5, [(2, 2), (3, 3), (1, 1)])
	solution = new_circuit.solve()
	print("Solution:")
	print(solution)
	new_circuit.print_circuit(solution)



