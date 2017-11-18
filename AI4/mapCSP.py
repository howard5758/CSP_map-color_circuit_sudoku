# Author: Ping-Jung Liu
# Date: October 14th 2017
# COSC 76 Assignment 4: Constraints Satisfaction Problems
# Acknowledgement: Professor Devin Balkom for providing suggestions 

from CSP import CSP

class mapCSP:

	def __init__(self, bt_mc, T, Color, Neighbors):

		# list of territories
		self.T = T
		# list of possible colors
		self.Color = Color
		# a set that indicates the neighbors of each territory
		self.Neighbors = Neighbors
		# 1 --> solve with backtracking   0 --> solve with min_conflict
		self.bt_mc = bt_mc
		

	def solve(self):

		X = []
		V = {}
		C = {}

		# get a list of different color pairs
		color_pairs = get_color_pairs(self.Color)

		# initialize variable and domain
		for i in range(0, len(self.T)):
			X.append(i)
			V[i] = []
			for c in self.Color:
				V[i].append(c)
			#V[i] = self.Color

		# initialize constraints
		for t in self.Neighbors:
			for n in self.Neighbors[t]:
				ti = self.T.index(t)
				ni = self.T.index(n)

				if not (ti, ni) in C and not (ni, ti) in C:
					C[(ti, ni)] = color_pairs

		#print(X)
		#print(V)
		#print(C)
		problem = CSP(X, V, C)

		# solve
		if self.bt_mc == 1:
			solution = problem.solve()
		else:
			solution = problem.min_conflicts(101)
		result = {}

		if solution == None:
			return None

		for idx in solution:
			result[self.T[idx]] = solution[idx]

		return result

def get_color_pairs(Color):

	pairs = []

	for i in range(0, len(Color)):
		for j in range(0, len(Color)):
			if not i == j:
				pairs.append((Color[i], Color[j]))

	return pairs

if __name__ == "__main__":

	new_map = mapCSP(1, ["WA", "NT", "Q", "SA", "NSW", "V", "T"], [1, 2, 3], {"WA":["NT", "SA"], "NT":["WA", "SA", "Q"], "SA":["WA", "NT", "Q", "NSW", "V"], "Q":["NT", "SA", "NSW"], "NSW":["Q", "SA", "V"], "V":["NSW", "SA"], "T":[]})
	#new_map = mapCSP(1, ["A", "B", "C", "D"], [1, 2], {"A":["B"], "B":["A", "C", "D"], "C":["B"], "D":["B"]})
	solution = new_map.solve()
	print("Solution:")
	print(solution)




