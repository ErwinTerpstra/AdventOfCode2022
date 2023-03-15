with open("day01_input.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]

	elves = [ ]

	currentElf = 0
	currentCalories = 0

	bestStockedElf = -1
	maxCalories = 0

	for line in lines:
		if len(line) == 0:
			elves.append({ "elf": currentElf, "calories": currentCalories });

			currentElf += 1
			currentCalories = 0
		else:
			currentCalories += int(line)


	elves.sort(key=lambda d: d["calories"], reverse=True)

	totalCalories = \
		elves[0]["calories"] + \
		elves[1]["calories"] + \
		elves[2]["calories"]

	print("Top three elves have " + str(totalCalories) + " calories")