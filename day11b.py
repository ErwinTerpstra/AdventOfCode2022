from functools import reduce

class Monkey:

	def __init__(self):
		self.inspection_count = 0

	def evaluateOperator(self, current_value, operand):
		return current_value if operand == None else operand

	def evaluate(self, current_value):
		lhs = self.evaluateOperator(current_value, self.operation_lhs)
		rhs = self.evaluateOperator(current_value, self.operation_rhs)

		new_value = (lhs + rhs) if self.operation_operator == '+' else (lhs * rhs)
		target_monkey = self.test_target_true if new_value % self.test_denominator == 0 else self.test_target_false

		self.inspection_count += 1

		return (target_monkey, new_value)
	
with open("day11_input.txt") as file:
	instructions = [ line.rstrip('\n') for line in file ]

monkeys = [ ]

# Parse monkey instructions
while len(instructions) > 0:
	instruction = instructions.pop(0)

	# Skip unexpected lines
	if not instruction.startswith('Monkey'):
		continue

	# Read all lines containing instructions for this monkey
	item_line = instructions.pop(0)
	operation_line = instructions.pop(0)
	test_line = instructions.pop(0)
	result_true_line = instructions.pop(0)
	result_false_line = instructions.pop(0)

	current_monkey = Monkey()

	# Parse items
	current_monkey.items = [ int(item.strip(' ')) for item in item_line.partition(':')[2].split(',') ]

	# Parse operation
	operationParts = operation_line.partition(':')[2].strip(' ').split(' ')
	current_monkey.operation_lhs = None if operationParts[2] == 'old' else int(operationParts[2])
	current_monkey.operation_rhs = None if operationParts[4] == 'old' else int(operationParts[4])
	current_monkey.operation_operator = operationParts[3]

	# Parse test
	current_monkey.test_denominator = int(test_line.split(' ')[-1])
	current_monkey.test_target_true = int(result_true_line.split(' ')[-1])
	current_monkey.test_target_false = int(result_false_line.split(' ')[-1])

	monkeys.append(current_monkey)

total_denominator = reduce(lambda a, b: a * b, [ monkey.test_denominator for monkey in monkeys ])

# Execute monkey shenanigans
# Simulate 10000 rounds
for round in range(10000):

	# Simulate each monkey in turn
	for i, monkey in enumerate(monkeys):

		for item in monkey.items:
			(target_monkey, adjusted_item) = monkey.evaluate(item)
			monkeys[target_monkey].items.append(adjusted_item % total_denominator)

		monkey.items.clear()

	print(f'Round {round} finished.')

# Print monkey activity
for i, monkey in enumerate(monkeys):
	print(f'Monkey {i} inspected items {monkey.inspection_count} times')

monkeys.sort(key=lambda monkey: monkey.inspection_count, reverse=True)

monkeyBusiness = monkeys[0].inspection_count * monkeys[1].inspection_count
print(f'Monkey business: {monkeyBusiness}')

print()