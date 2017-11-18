# Author: Ping-Jung Liu
# Date: October 14th 2017
# COSC 76 Assignment 4: Constraints Satisfaction Problems
# Acknowledgement: Professor Devin Balkom for providing suggestions 

from CSP import CSP

# for printing clarity
def revise_components(Components):

	for i in range(0, len(Components)):
		(x, y, xx, yy, shift) = Components[i]
		Components[i] = (xx, yy, x, y, -shift)

	return Components

class new_circuitCSP:

	# in this version, a component is defined with two rectangles
	# one bot and one up
	# and a integer indicating the shift between the two
	# ex. (2, 1, 3, 1, 0)
	# aaa
	# aa
	# ex. (4, 2, 2, 1, 3)
	#    aa
	# aaaa
	# aaaa
	def __init__(self, width, height, Components):
		self.width = width
		self.height = height
		self.Components = revise_components(Components)

	# though initializing X V C are tedious, the idea is straightforward
	# so I will not go into the details
	# feel free to modify the test cases below
	def solve(self):

		X = []
		V = {}
		C = {}

		for i in range(0, len(self.Components)):
			X.append(i)

			bot_width = self.Components[i][0]
			bot_height = self.Components[i][1]
			up_width = self.Components[i][2]
			up_height = self.Components[i][3]
			shift = self.Components[i][4]

			for x in range(0, self.width):
				for y in range(0, self.height):

					if x + shift >= 0 and x + bot_width <= self.width and x + shift + up_width <= self.width and y + bot_height + up_height <= self.height:
						if i in V:
							V[i].append((x, y))
						else:
							V[i] = [(x, y)]

		for i in range(0, len(X)):
			for j in range(0, len(X)):
				if not i == j:
					if not (i, j) in C and not (j, i) in C:
						C[(i, j)] = self.get_cons(i, j, V)

		#print(X)
		#print(V)
		#rint(C)

		problem = CSP(X, V, C)

		solution = problem.solve()
		result = {}
		#print(solution)
		if solution == None:
			return None

		for idx in solution:
			result[tuple(self.Components[idx])] = solution[idx]

		return result

	def get_cons(self, i, j, V):
		width = self.width
		height = self.height
		c = []

		for vi in V[i]:
			for vj in V[j]:

				i_bot_lb = vi
				i_bot_ru = (vi[0] + self.Components[i][0] - 1, vi[1] + self.Components[i][1] - 1)
				i_up_lb = (vi[0] + self.Components[i][4], vi[1] + self.Components[i][1])
				i_up_ru = (i_up_lb[0] + self.Components[i][2] - 1, i_up_lb[1] + self.Components[i][3] - 1)
				j_bot_lb = vj
				j_bot_ru = (vj[0] + self.Components[j][0] - 1, vj[1] + self.Components[j][1] - 1)
				j_up_lb = (vj[0] + self.Components[j][4], vj[1] + self.Components[j][1])
				j_up_ru = (j_up_lb[0] + self.Components[j][2] - 1, j_up_lb[1] + self.Components[j][3] - 1)

				if self.safe(i_bot_lb, i_bot_ru, j_bot_lb, j_bot_ru) and self.safe(i_bot_lb, i_bot_ru, j_up_lb, j_up_ru) and self.safe(i_up_lb, i_up_ru, j_bot_lb, j_bot_ru) and self.safe(i_up_lb, i_up_ru, j_up_lb, j_up_ru):
					c.append((vi, vj))

		return c

	def safe(self, i_lb, i_ru, j_lb, j_ru):
		return i_lb[0] > j_ru[0] or j_lb[0] > i_ru[0] or i_ru[1] < j_lb[1] or j_ru[1] < i_lb[1]

	def print_circuit(self, solution):

		if solution == None:
			print("No Solution")
		else:
			for j in range(0, self.height):
				for i in range(0, self.width):
					p = False
					for component in solution:

						if self.in_range(i, j, component, solution):	
							print(self.Components.index(component), end='')
							p = True
							break
					if not p:
						print("#", end='')
				print("")


	def in_range(self, i, j, component, solution):

		sol_bot = solution[component]
		sol_up = (solution[component][0] + component[4], solution[component][1] + component[1])

		good = 0

		if i >= sol_bot[0] and i < sol_bot[0] + component[0] and j >= sol_bot[1] and j < sol_bot[1] + component[1]:
			good = good +1
		if i >= sol_up[0] and i < sol_up[0] + component[2] and j >= sol_up[1] and j < sol_up[1] + component[3]:
			good = good +1

		return good > 0




if __name__ == "__main__":

	new_circuit = new_circuitCSP(10, 10, [(2, 1, 1, 2, 1), (10, 1, 4, 5, 6), (3, 3, 4, 2, 0), (6, 1, 3, 1, 3), (3, 2, 2, 2, 1), (4, 3, 5, 1, 0)])
	#new_circuit = new_circuitCSP(5, 5, [(3, 1, 1, 4, 0), (2, 1, 2, 2, -1), (2, 2, 1, 3, 1)])
	solution = new_circuit.solve()
	new_circuit.print_circuit(solution)
	