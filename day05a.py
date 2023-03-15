from parse import *

with open("day05_input.txt") as file:
	stacks = [ ]
	lines = [ line for line in file ]
	
	# Search for the empty line
	separator = lines.index('\n')
	
	# Parse lines containing stacks (-2 to exclude the stack number labels, reverse to ensure correct order)
	for line in lines[separator - 2::-1]:
		for index, crate in enumerate(line[1::4]):
			if crate == ' ':
				continue

			# Make sure there's enough stacks registered
			while len(stacks) <= index:
				stacks.append([])

			stacks[index].append(crate)
			
	# Parse lines containing instructions
	for line in lines[separator + 1:]:
		instruction = parse('move {amount} from {src} to {dst}', line)

		amount = int(instruction['amount'])
		src = int(instruction['src']) - 1
		dst = int(instruction['dst']) - 1

		for i in range(0, amount):
			stacks[dst].append(stacks[src].pop())

	# Print top stack crates
	print("".join(stack[-1] for stack in stacks))