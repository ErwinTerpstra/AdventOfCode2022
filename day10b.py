with open("day10_input.txt") as file:
	instructions = [ line.rstrip('\n') for line in file ]
	
	reg_x = 1
	next_x = reg_x

	cycles = 1
	display_cycles = 1
	display_buffer = ''

	for instruction in instructions:
		if instruction.startswith('add'):
			(opcode, parameter0) = instruction.split(' ')
			next_x = reg_x + int(parameter0)
			cycles += 2
		else:
			cycles += 1

		while display_cycles < cycles:
			display_x = (display_cycles - 1) % 40

			sprite_is_visible = abs(display_x - reg_x) <= 1

			display_buffer += '#' if sprite_is_visible else '.'
			display_cycles += 1

			if display_x == 39:
				print(display_buffer)
				display_buffer = ''

		reg_x = next_x
