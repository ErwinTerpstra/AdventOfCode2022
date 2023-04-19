from collections import namedtuple
from typing import overload

DIRECTION_RIGHT = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_UP = 3

TILE_EMPTY = 0
TILE_OPEN = 1
TILE_WALL = 2

Point = namedtuple('Point', 'x y')

tiles = \
{
	' ': TILE_EMPTY,
	'.': TILE_OPEN,
	'#': TILE_WALL
}

directions = \
[
	Point( 1,  0),
	Point( 0,  1),
	Point(-1,  0),
	Point( 0, -1),
]

tileCharacters = list(tiles.keys())
directionCharacters = [ '>', 'v', '<', '^' ]

offset = \
[
	[ ], # Right
	[ ], # Bottom
	[ ], # Left
	[ ], # Top
]

instructions = [ ]
grid = [ ]
visitedLocations = { }

def grid_get(x, y):
	return grid[y * width + x]

def grid_in_bounds(x, y):
	return x >= 0 and x < width and y >= 0 and y < height

def wrap(point, direction):
	if direction == DIRECTION_LEFT or direction == DIRECTION_RIGHT:
		return Point(offset[direction][point.y], point.y)
	else: # if direction == DIRECTION_UP or direction == DIRECTION_DOWN
		return Point(point.x, offset[direction][point.x])

def next_position(position, direction):
	offset = directions[direction]
	next = Point(position.x + offset.x, position.y + offset.y)

	if not grid_in_bounds(next.x, next.y) or grid_get(next.x, next.y) == TILE_EMPTY:
		next = wrap(next, direction)

	return next

def get_tile_character(tile):
	return tileCharacters[tile]

def print_grid():
	for y in range(height):
		line = ''

		for x in range(width):
			previousDirection = visitedLocations.get(Point(x, y), None)
			
			if previousDirection == None:
				line += get_tile_character(grid_get(x, y))
			else:
				line += directionCharacters[previousDirection]

		print(line)

	print()

# Read input
with open('day22_input.txt') as file:
	lines = [ line.rstrip('\n') for line in file ]
	
	gridLines = lines[:-2]
	instructionsLine = lines[-1]

# Parse grid
width = max([ len(line) for line in gridLines ])
height = len(gridLines)

for line in gridLines:
	# Add tiles to grid
	grid.extend([ tiles[c] for c in line ])

	# Padd until end of line
	grid.extend([ TILE_EMPTY ] * (width - len(line)))

# Parse instructions
distanceBuffer = 0
for c in instructionsLine:
	if c.isdigit():
		distanceBuffer = distanceBuffer * 10 + int(c)
	else:
		if distanceBuffer > 0:
			instructions.append(distanceBuffer)
			distanceBuffer = 0

		instructions.append(c)

if distanceBuffer > 0:
	instructions.append(distanceBuffer)

# Parse grid spacing
for y in range(height):
	# Horizontal from left to right
	for x in range(width):
		if grid_get(x, y) != TILE_EMPTY:
			break

	offset[DIRECTION_RIGHT].append(x)
	
	# Horizontal from right to left
	for x in reversed(range(width)):
		if grid_get(x, y) != TILE_EMPTY:
			break

	offset[DIRECTION_LEFT].append(x)

for x in range(width):
	# Vertical from top to bottom
	for y in range(height):
		if grid_get(x, y) != TILE_EMPTY:
			break

	offset[DIRECTION_DOWN].append(y)
	
	# Vertical from bottom to top
	for y in reversed(range(height)):
		if grid_get(x, y) != TILE_EMPTY:
			break

	offset[DIRECTION_UP].append(y)

print(instructions)

# Initial setup
position = Point(offset[DIRECTION_LEFT][0], 0)
direction = DIRECTION_RIGHT

# Simulate instructions
for instruction in instructions:
	if isinstance(instruction, int):
		# Move ahead for N units
		for i in range(instruction):
			visitedLocations[position] = direction 
			#print_grid()

			# Determine at the next position
			next = next_position(position, direction)

			# If it is blocked, stop here
			if grid_get(next.x, next.y) == TILE_WALL:
				break

			# Move to the next position
			position = next

	else:
		# Rotate R (CW) or L (CCW)
		rotation = 1 if instruction == 'R' else -1
		direction = (direction + rotation + 4) % 4

	#print()

password = (position.y + 1) * 1000 + (position.x + 1) * 4 + direction
print(f'Password: {password}')