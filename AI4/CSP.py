# Author: Ping-Jung Liu
# Date: October 14th 2017
# COSC 76 Assignment 4: Constraints Satisfaction Problems
# Acknowledgement: Professor Devin Balkom for providing suggestions 

from datetime import datetime
from math import inf
from collections import deque
import random

class CSP:

	def __init__(self, X, V, C):

		self.tryy = 0
		self.nodes_visited = 0
		# variable
		self.X = X
		# value domain
		self.V = V
		# constraints
		self.C = C
		(self.arc, self.graph) = get_arcgraph(X, V, C)

		# switch on and off to test
		self.MRV = True
		self.LCV = False
		self.MAC = False
		self.Enforced_AC = True

	# backtracking solver
	def solve(self):

		# run ac3 for all arc
		if self.Enforced_AC:
			first_ac3 = True
			arc_que = deque()
			for arc in self.arc:
				arc_que.append(arc)
			first_ac3 = self.ac3(arc_que, {}, False)
			if not first_ac3:
				return None

		now = datetime.now()

		solution = self.backtracking({})

		after = datetime.now()


		print("Time Spent:")
		print(after - now)
		print("Nodes Visited:")
		print(self.nodes_visited)
		print("Try:")
		print(self.tryy)
		return solution

	# backtracking
	def backtracking(self, partial_sol):
		
		self.nodes_visited = self.nodes_visited + 1

		if len(partial_sol) == len(self.V):
			return partial_sol

		# select an unassigned variable
		var = self.suv(partial_sol)
		#print(var)
		# order the domain values
		ord_value = self.order_domain(var, partial_sol)

		# loop through values
		for i in range(0, len(ord_value)):
			value = ord_value[i]
			# to recover deleted domains if value is bad
			removed = {}

			self.tryy = self.tryy + 1
			# check if assignment is consistent
			if self.consistent(var, value, partial_sol) and not var in partial_sol:

				partial_sol[var] = value

				# if inference returns true, continue backtracking
				if self.inference(var, value, partial_sol, removed):
				
					next_sol = self.backtracking(partial_sol)
					if not next_sol == None:
						return next_sol

			# add removed back to domain
			for re_var in removed:
				self.V[re_var] = list(set(self.V[re_var] + removed[re_var]))

			if var in partial_sol:
				del partial_sol[var]
		return None



	# select unassigned variable
	def suv(self, partial_sol):

		min_size = inf

		# look for the variable with least domain size
		for var in self.X:
			if not var in partial_sol:
				if self.MRV:
					if len(self.V[var]) < min_size:
						min_size = len(self.V[var])
						mrv_var = var 
				else:
					return var

		return mrv_var

	def order_domain(self, var, partial_sol):

		if not self.LCV:

			temp_V = []
			for v in self.V[var]:
				temp_V.append(v)
			return temp_V

		# order the domain so that values with less conflicts come first
		else:
			rank = []

			for val in self.V[var]:
				count = 0

				if var in self.graph:
					for neighbor in self.graph[var]:
						for n_val in self.V[neighbor]:
							if (neighbor, var) in self.C and not (n_val, val) in self.C[(neighbor, var)]:
								count = count + 1
							elif (var, neighbor) in self.C and not (val, n_val) in self.C[(var, neighbor)]:			
								count = count + 1

				rank.append((count, val))

		rank.sort()

		result = []
		for i in range(0, len(rank)):
			result.append(rank[i][1])
		return result

	def inference(self, var, value, partial_sol, removed):

		# add related values to removed
		if var in removed:
			removed[var] = list(set(removed[var] + self.V[var]))
		else:
			removed[var] = self.V[var]

		# remove all other value except the guess value
		self.V[var] = [value]

		if not self.MAC:
			return True
		else:

			# perform ac3 on all arc(j, i)
			arc_que = deque()
			for arc in self.arc:
				if not arc[0] in partial_sol and arc[1] == var:
					arc_que.append(arc)

			return self.ac3(arc_que, removed, True)

	# arc consistent 3
	def ac3(self, arc_que, removed, infer):

		while len(arc_que) > 0:
			arc = arc_que.pop()

			# if revised, add all related arc to the que
			if self.revise(arc, removed, infer):

				if len(self.V[arc[0]]) == 0:
					return False
				elif arc[0] in self.graph:
					for neighbor in self.graph[arc[0]]:
						if not neighbor == arc[1]:
							arc_que.append((neighbor, arc[0]))
		return True

	# revise the domain so that there is no conflict
	def revise(self, arc, removed, infer):

		revised = False

		for val in self.V[arc[0]]:
			
			good_val = False

			for n_val in self.V[arc[1]]:
				if (arc[0], arc[1]) in self.C and (val, n_val) in self.C[(arc[0], arc[1])]:
					good_val = True
					#break
				if (arc[1], arc[0]) in self.C and (n_val, val) in self.C[(arc[1], arc[0])]:
					good_val = True
					#break

			if not good_val:

				revised = True
				self.V[arc[0]].remove(val)

				if infer:
					if arc[0] in removed:
						removed[arc[0]] = list(set(removed[arc[0]] + [val]))
					else:
						removed[arc[0]] = [val]
		return revised

	# check if an assignment is consistent
	def consistent(self, var, value, partial_sol):

		if var in self.graph:
			for neighbor in self.graph[var]:
				if neighbor in partial_sol:
					
					if (var, neighbor) in self.C and not (value, partial_sol[neighbor]) in self.C[(var, neighbor)]:
						return False
					elif (neighbor, var) in self.C and not (partial_sol[neighbor], value) in self.C[(neighbor, var)]:
						return False

		return True

	# min_conflicts solver
	def min_conflicts(self, max_steps):

		partial_sol = {}

		# can either randomly select initial solution or use greedy method
		now = datetime.now()
		for var in self.X:

			partial_sol[var] = self.best_val(var, partial_sol)
			#partial_sol[var] = self.V[var][0]

		for i in range(0, max_steps):
			print(i)
			if self.is_solution(partial_sol):
				print("steps:")
				print(i)
				after = datetime.now()
				print("Time Spent:")
				print(after - now)
				return partial_sol

			# randomly select a conflicted variable
			possible_var = []

			for var in self.X:
				if self.conflicts(var, partial_sol[var], partial_sol) > 0:
					possible_var.append(var)
			
			next_var = random.choice(possible_var)
			# modify solution
			partial_sol[next_var] = self.best_val(next_var, partial_sol)

		return None

	# check if partial_sol is solution
	def is_solution(self, partial_sol):

		for var in partial_sol:
			if self.conflicts(var, partial_sol[var], partial_sol) > 0:
				return False

		return True

	# return the value with least conflicts
	def best_val(self, var, partial_sol):

		min_conf = inf

		for val in self.V[var]:
			if self.conflicts(var, val, partial_sol) < min_conf:
				min_conf = self.conflicts(var, val, partial_sol)
				best_val = val

		return best_val

	# calculate the conflicts of a value
	def conflicts(self, var, val, partial_sol):

		conf = 0

		for assign in partial_sol:
			if (var, assign) in self.C and not (val, partial_sol[assign]) in self.C[(var, assign)]:
				conf = conf + 1
			elif (assign, var) in self.C and not (partial_sol[assign], val) in self.C[(assign, var)]:
				conf = conf + 1

		return conf

# generate the arc and graph of a CSP 
def get_arcgraph(X, V, C):

	arc = []
	graph = {}

	for (one, two) in C:
		arc.append((one, two))
		arc.append((two, one))

		if one in graph:
			graph[one].append(two)
		else:
			graph[one] = [two]

		if two in graph:
			graph[two].append(one)
		else:
			graph[two] = [one]

	return (arc, graph)