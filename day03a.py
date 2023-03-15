with open("day03_input.txt") as file:
	rucksacks = [ list(line.rstrip('\n')) for line in file ]
	totalPriority = 0
	
	for rucksack in rucksacks:
		compartmentSize = int(len(rucksack) / 2)
	
		left = rucksack[:compartmentSize]
		right = rucksack[compartmentSize:]

		duplicate = next(item for item in left if item in right)
		lowercase = duplicate >= 'a'

		priority = ord(duplicate) - ord('a' if lowercase else 'A') + 1

		if not lowercase:
			priority += 26

		totalPriority += priority

	print(totalPriority)