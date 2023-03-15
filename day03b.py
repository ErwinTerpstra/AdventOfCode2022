def chunks(list, size):
    return (list[pos:pos + size] for pos in range(0, len(list), size))

with open("day03_input.txt") as file:
	rucksacks = [ list(line.rstrip('\n')) for line in file ]
	totalPriority = 0
	
	for group in chunks(rucksacks, 3):
		duplicate = next(item for item in group[0] if item in group[1] and item in group[2])
		lowercase = duplicate >= 'a'

		priority = ord(duplicate) - ord('a' if lowercase else 'A') + 1

		if not lowercase:
			priority += 26

		totalPriority += priority

	print(totalPriority)