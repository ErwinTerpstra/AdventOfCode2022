with open("day04_input.txt") as file:
	pairs = [ line.rstrip('\n').split(',') for line in file ]

	overlappingPairs = 0

	for pair in pairs:
		first = [ int(value) for value in pair[0].split('-') ]
		second = [ int(value) for value in pair[1].split('-') ]

		overlap = (first[0] <= second[0] and first[1] >= second[1]) or \
				  (first[0] <= second[0] and first[1] >= second[0]) or \
				  (first[0] <= second[1] and first[1] >= second[1]) or \
				  (first[0] >= second[0] and first[1] <= second[1])
		
		if overlap:
			overlappingPairs += 1

	print(overlappingPairs)