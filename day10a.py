with open("day10_input.txt") as file:
	instructions = [ line.rstrip('\n') for line in file ]
	
	log_cycles = [ 20, 60, 100, 140, 180, 220 ]

	reg_x = 1

	cycles = 1
	accumulator = 0

	for instruction in instructions:
		prev_x = reg_x

		if instruction.startswith('add'):
			(opcode, parameter0) = instruction.split(' ')
			reg_x += int(parameter0)
			cycles += 2
		else:
			cycles += 1

		log_cycle = log_cycles[0]

		if cycles > log_cycle:			
			signal_strength = log_cycle * prev_x
			accumulator += signal_strength

			print(f'Cycle #{log_cycle}: {signal_strength}')

			log_cycles.pop(0)

			if len(log_cycles) == 0:
				break

	print(accumulator)