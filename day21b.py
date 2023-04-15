def op_add(lhs, rhs):
	return lhs + rhs

def op_sub(lhs, rhs):
	return lhs - rhs

def op_mul(lhs, rhs):
	return lhs * rhs

def op_div(lhs, rhs):
	return lhs // rhs

operators = \
{
	'+': op_add,
	'-': op_sub,
	'*': op_mul,
	'/': op_div
}

inverse_operators = \
{
	'+': op_sub,
	'-': op_add,
	'*': op_div,
	'/': op_mul
}

class Monkey:
	def __init__(self, id, command):
		self.id = id
		
		self.lhs = None
		self.rhs = None

		if command.isdigit():
			self.value = int(command)
			self.op = None

			self.monkeyL = None
			self.monkeyR = None

		else:
			lhs, op, rhs = command.split(' ')
			
			self.value = None
			self.op = op

			self.monkeyL = lhs
			self.monkeyR = rhs

	def eval(self):
		if self.id == 'humn':
			return None
		
		if self.value == None:
			# Evaluate both child branches, store results
			self.lhs = self.monkeyL.eval()
			self.rhs = self.monkeyR.eval()

			# If one of then contains None, that is the branch containing the human and we can't calculate the branch result yet
			# Other we apply our operator method
			if self.lhs != None and self.rhs != None:
				self.value = operators[self.op](self.lhs, self.rhs)

		return self.value

	def solve_root(self):
		# Evaluate both branches to check which one is unknown
		self.lhs = self.monkeyL.eval()
		self.rhs = self.monkeyR.eval()

		# Root monkey has the special equals operator, so we solve the unknown branch against the value of the other
		if self.lhs == None:
			return self.monkeyL.solve(self.rhs)
		
		if self.rhs == None:
			return self.monkeyR.solve(self.lhs)
		
		raise Exception('Both branches known, should not happen')
	
	def solve(self, expectedValue):
		# If we reached the human, we know what they have to say
		if self.id == 'humn':
			return expectedValue
		
		# We shouldn't try to solve branches with known values
		if self.value != None:
			raise Exception('solve() should only be called on unsolved branches')
		
		# This only happens for "unsolved" branches, so the human is either in lhs or rhs
		# Check which one is defined and calculate the difference with "expectedValue"
		if self.lhs == None:
			# Human in LHS, we can just use inverse operators

			# lhs + rhs => expectedValue - rhs
			# lhs - rhs => expectedValue + rhs
			# lhs * rhs => expectedValue / lhs
			# lhs / rhs => expectedValue * rhs

			expectedValue = inverse_operators[self.op](expectedValue, self.rhs)
			return self.monkeyL.solve(expectedValue)
		
		if self.rhs == None:
			# Human in RHS, different operators need to be handled differently

			# lhs + rhs => expectedValue - lhs
			# lhs - rhs => lhs - expectedValue
			# lhs * rhs => expectedValue / lhs
			# lhs / rhs => lhs / expectedValue

			if self.op == '-' or self.op == '/':
				expectedValue = operators[self.op](self.lhs, expectedValue)
			else: # self.op == '+' or self.op == '*'
				expectedValue = inverse_operators[self.op](expectedValue, self.lhs)
				
			return self.monkeyR.solve(expectedValue)
		
		raise Exception('Both branches known, should not happen')

monkeys = { }

# Parse input
with open('day21_input.txt') as file:
	for line in file:
		id, command = line.rstrip('\n').split(': ')
		
		monkeys[id] = Monkey(id, command)

	# Resolve monkey references
	for monkey in monkeys.values():
		monkey.monkeyL = monkeys[monkey.monkeyL] if monkey.monkeyL else None
		monkey.monkeyR = monkeys[monkey.monkeyR] if monkey.monkeyR else None

# Calculate result
rootMonkey = monkeys['root']

# Solve for "humn"
result = rootMonkey.solve_root()

print(f'Human must say: {result}')