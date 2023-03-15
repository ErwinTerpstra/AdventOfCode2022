with open("day01_input.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]

	currentElf = 0
	currentCalories = 0

	bestStockedElf = -1
	maxCalories = 0

	for line in lines:
		if len(line) == 0:
			if currentCalories > maxCalories:
				bestStockedElf = currentElf
				maxCalories = currentCalories

			currentElf += 1
			currentCalories = 0
		else:
			currentCalories += int(line)

	print("Elf with most calories: " + str(bestStockedElf) + " (" + str(maxCalories) + ")")