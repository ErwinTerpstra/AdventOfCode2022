		

with open("day08_input.txt") as file:
	grid =  [ [ int(c) for c in line.rstrip('\n') ] for line in file ]
	
	width = len(grid[0])
	height = len(grid)

	def calculateVisibility(x, y):
		treeHeight = grid[y][x]
		left = right = top = bottom = 0
		
		# Left
		for xx in range(x - 1, -1, -1):
			left += 1
			if grid[y][xx] >= treeHeight:
				break

		# Right
		for xx in range(x + 1, width):
			right += 1
			if grid[y][xx] >= treeHeight:
				break
		
		# Top
		for yy in range(y - 1, -1, -1):
			top += 1
			if grid[yy][x] >= treeHeight:
				break

		# Bottom
		for yy in range(y + 1, height):
			bottom += 1
			if grid[yy][x] >= treeHeight:
				break

		return left * right * top * bottom
	
	highestVisibility = 0

	for y in range(0, height):
		for x in range(0, width):
			visibility = calculateVisibility(x, y)
			highestVisibility = max(visibility, highestVisibility)

	print(highestVisibility)