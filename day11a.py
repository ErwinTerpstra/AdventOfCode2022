class Monkey:

	def __init__(self):
		self.inspectionCount = 0

	def evaluateOperator(self, currentValue, operand):
		if operand == 'old':
			return currentValue
		else:
			return int(operand)

	def evaluate(self, currentValue):
		print(f'  Monkey inspects an item with a worry level of {currentValue}')

		lhs = self.evaluateOperator(currentValue, self.operation['lhs'])
		rhs = self.evaluateOperator(currentValue, self.operation['rhs'])

		results = \
		{
			'+': lhs + rhs,
			'-': lhs - rhs,
			'*': lhs * rhs,
			'/': lhs / rhs,
		}

		newValue = results[self.operation['operator']]
		print(f'    Worry level changes to {newValue}')
		
		newValue = int(newValue / 3)		
		print(f'    Monkey gets bored with item. Worry level is divided by 3 to {newValue}')

		targetMonkey = self.test['targets'][newValue % self.test['denominator'] == 0]
		print(f'    Item with worry level {newValue} is thrown to monkey {targetMonkey}')

		self.inspectionCount += 1

		return (targetMonkey, newValue)
	
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
	itemLine = instructions.pop(0)
	operationLine = instructions.pop(0)
	testLine = instructions.pop(0)
	resultTrueLine = instructions.pop(0)
	resultFalseLine = instructions.pop(0)

	currentMonkey = Monkey()

	# Parse items
	currentMonkey.items = [ int(item.strip(' ')) for item in itemLine.partition(':')[2].split(',') ]

	# Parse operation
	operationParts = operationLine.partition(':')[2].strip(' ').split(' ')
	currentMonkey.operation = \
	{
		'lhs': operationParts[2],
		'rhs': operationParts[4],

		'operator': operationParts[3],
	}

	# Parse test
	currentMonkey.test = \
	{
		'denominator': int(testLine.split(' ')[-1]),
		'targets': 
		{
			True: int(resultTrueLine.split(' ')[-1]),
			False: int(resultFalseLine.split(' ')[-1])
		}
	}

	monkeys.append(currentMonkey)

# Execute monkey shenanigans
# Simulate 20 rounds
for round in range(20):

	# Simulate each monkey in turn
	for i, monkey in enumerate(monkeys):
		print(f'Monkey {i}:')

		for item in monkey.items:
			(targetMonkey, adjustedItem) = monkey.evaluate(item)
			monkeys[targetMonkey].items.append(adjustedItem)

		monkey.items = [ ]


	# Print monkey states
	print(f'After round {round + 1}, the monkeys are holding items with these worry levels:')
	for i, monkey in enumerate(monkeys):
		print(f'Monkey {i}: {", ".join([ str(item) for item in monkey.items ])}')

	print()


# Print monkey activity
for i, monkey in enumerate(monkeys):
	print(f'Monkey {i} inspected items {monkey.inspectionCount} times')

monkeys.sort(key=lambda monkey: monkey.inspectionCount, reverse=True)

monkeyBusiness = monkeys[0].inspectionCount * monkeys[1].inspectionCount
print(f'Monkey business: {monkeyBusiness}')

print()