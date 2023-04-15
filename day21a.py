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

class Monkey:
	def __init__(self, id, command):
		self.id = id
		
		if command.isdigit():
			self.value = int(command)
		else:
			lhs, op, rhs = command.split(' ')
			
			self.value = None
			self.lhs = lhs
			self.rhs = rhs
			self.op = operators[op]

	def eval(self, monkeys):
		if self.value == None:
			self.value = self.op(monkeys[self.lhs].eval(monkeys), monkeys[self.rhs].eval(monkeys))

		return self.value

monkeys = { }

# Parse input
with open('day21_input.txt') as file:
	for line in file:
		id, command = line.rstrip('\n').split(': ')
		
		monkeys[id] = Monkey(id, command)

# Calculate result
result = monkeys['root'].eval(monkeys)
print(f'Root monkey says: {result}')