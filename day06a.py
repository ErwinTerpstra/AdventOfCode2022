with open("day06_input.txt") as file:
	data = file.read()
	i = 0
	
	while True:
		characters = data[i:i+4]
		if len(set(characters)) == 4:
			break

		i += 1

	print(i + 4)