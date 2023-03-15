		

with open("day08_input.txt") as file:
	grid =  [ [ int(c) for c in line.rstrip('\n') ] for line in file ]
	
	width = len(grid[0])
	height = len(grid)

	visibleTrees = 0
	
	def isTreeVisible(x, y):
		treeHeight = grid[y][x]
		visibleDirections = 4
		
		# Left
		for xx in range(0, x):
			if grid[y][xx] >= treeHeight:
				visibleDirections -= 1
				break

		# Right
		for xx in range(x + 1, width):
			if grid[y][xx] >= treeHeight:
				visibleDirections -= 1
				break
		
		# Top
		for yy in range(0, y):
			if grid[yy][x] >= treeHeight:
				visibleDirections -= 1
				break

		# Bottom
		for yy in range(y + 1, height):
			if grid[yy][x] >= treeHeight:
				visibleDirections -= 1
				break

		return visibleDirections > 0

	for y in range(0, height):
		for x in range(0, width):
			if isTreeVisible(x, y):
				visibleTrees += 1

	print(visibleTrees)