import os
import time

sandSpawn = (500, 0)
consideredDirections = \
[
	( 0, 1),
	(-1, 1),
	( 1, 1),
]

air = '.'
rock = '#'
sand = 'o'

def get_index(position):
	return (position[1] - minY) * width + (position[0] - minX)

def grid_get(position):
	return grid[get_index(position)]

def grid_set(position, material):
	grid[get_index(position)] = material

def sign(x):
	return (x > 0) - (x < 0)

def print_grid():
	text = ''
	for y in range(minY, maxY + 1):
		for x in range(minX, maxX + 1):
			text += grid[get_index((x, y))]

		text += '\n'

	text += f'Sand at rest: {sandAtRest}\n'

	print(text)

with open("day14_input.txt") as file:
	paths = [ [ tuple(int(value) for value in position.split(',')) for position in line.rstrip('\n').split(' -> ') ] for line in file ]

# Determine grid bounds
minX = sandSpawn[0]
maxX = sandSpawn[0]
minY = sandSpawn[1]
maxY = sandSpawn[1]

for path in paths:
	for position in path:
		minX = min(minX, position[0])
		minY = min(minY, position[1])
		maxX = max(maxX, position[0])
		maxY = max(maxY, position[1])

width = maxX - minX + 1
height = maxY - minY + 1

grid = [ ]
sandAtRest = 0

# Create an empty grid
for y in range(minY, maxY + 1):
	for x in range(minX, maxX + 1):
		grid.append(air)

# Rasterize stone paths
for path in paths:
	for i in range(len(path) - 1):
		start = path[i]
		end = path[i + 1]

		dx = end[0] - start[0]
		dy = end[1] - start[1]

		sx = sign(dx)
		sy = sign(dy)

		current = start

		print(f'{start} to {end}')

		while current[0] != end[0] or current[1] != end[1]:
			grid_set(current, rock)
			current = (current[0] + sx, current[1] + sy)
		
		grid_set(current, rock)

print_grid()
os.system("pause")

# Simulate sand
while True:
	sandPos = sandSpawn

	while sandPos[0] >= minX and sandPos[0] <= maxX and sandPos[1] <= maxY:
		grid_set(sandPos, sand)

		# Move the sand down
		direction = None
		for potentialDirection in consideredDirections:
			newSandPos = (sandPos[0] + potentialDirection[0], sandPos[1] + potentialDirection[1])

			# Check if this direction is in bounds
			if sandPos[0] >= minX and sandPos[0] <= maxX and sandPos[1] <= maxY:
				# Check if this direction is blocked
				if grid_get(newSandPos) != air:
					continue

			direction = potentialDirection
			break

		# Check if we found a valid direction
		if direction != None:
			grid_set(sandPos, air)
			sandPos = (sandPos[0] + direction[0], sandPos[1] + direction[1])
		else:
			sandAtRest += 1
			break


	#os.system('cls')
	print_grid()
		
