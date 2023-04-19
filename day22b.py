from collections import namedtuple
from typing import overload

DR = 0
DD = 1
DL = 2
DU = 3

TILE_NULL = 0
TILE_PATH = 1
TILE_WALL = 2

Point = namedtuple('Point', [ 'x', 'y' ])


# 	Example:			Input:
# 	. . 1 .				. 1 2 .
# 	2 3 4 .				. 3 . .
# 	. . 5 6				4 5 . .
# 	. . . .				6 . . .
#



# 	.. .. 02 ..			.. 01 02 ..
# 	04 05 06 ..			.. 05 .. ..
# 	.. .. 10 11			08 09 .. ..
# 	.. .. .. ..			12 .. .. ..



# Input
edges = \
[
	# Column
	# Right, Down, Left, Up
	# Column 0								Column 1						Column 2								Column 3
	None,									[ 2, 5, (8, DR), (12, DR) ],	[ (9, DL), (5, DL), 1, (12, DU) ],		None								,
	None,									[ (2, DU), 9, (8, DD), 1 ],		None,									None 								,
	[ 9, 12, (1, DR), (5, DR) ],			[ (2, DL), (12, DL), 8, 5 ],	None,									None 								,
	[ (9, DU), (2, DD), (1, DD), 8 ],		None,							None,									None 								,
]

'''
# Example
edges = \
[
	# Column
	# Right, Down, Left, Up
	# Column 0								Column 1						Column 2								Column 3
	None,									None,							[ (11, DL), 6, (5, DD), (4, DD) ],		None								,
	[ 5, (10, DU), (11, DU), (2, DD) ],		[ 6, (10, DR), 4, (2, DR) ],	[ (11, DD), 10, 5, 2 ],					None								,
	None,									None, 							[ 11, (4, DU), (5, DU), 6 ],			[ (2, DL), (4, DR), 10, (6, DL) ]	,
	None,									None,							None,									None 								,
]
'''


tiles = \
{
	' ': TILE_NULL,
	'.': TILE_PATH,
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

instructions = [ ]
grid = [ ]
visitedLocations = { }

def grid_get(x, y):
	return grid[y * width + x]

def grid_in_bounds(x, y):
	return x >= 0 and x < width and y >= 0 and y < height

def plane_index(x, y):
	return (y // planeSize) * 4 + (x // planeSize)

def world_to_local(x, y):
	return Point(x % planeSize, y % planeSize)

def local_to_world(plane, x, y):
	return Point((plane % 4) * planeSize + x, (plane // 4) * planeSize + y)

def rotate(point, amount):
	while amount > 0:
		point = Point(planeSize - 1 - point.y, point.x)
		amount -= 1

	return point

def next_position(current, currentDirection):
	offset = directions[currentDirection]

	next = Point(current.x + offset.x, current.y + offset.y)

	# Check if this movement takes us to a differnt plane
	currentPlane = plane_index(current.x, current.y)
	nextPlane = plane_index(next.x, next.y)

	if currentPlane != nextPlane:
		edgeData = edges[currentPlane]

		# Sanity check
		if edgeData == None:
			print_grid()
			raise Exception(f'Attempting to access invalid plane {currentPlane}')

		directionData = edgeData[currentDirection]

		# Calculate the local position within the next plane
		local = world_to_local(next.x, next.y)

		if isinstance(directionData, tuple):
			# Tuple plane data means there is a plane index and direction defined
			nextPlane, nextDirection = directionData

			# Calculate the relative rotation
			deltaDirection = (nextDirection - direction + 4) % 4

			# Rotate the local position within the plane
			local = rotate(local, deltaDirection)
		elif isinstance(directionData, int):
			# Integer plane references means the direction does not change
			nextPlane = directionData
			nextDirection = currentDirection
		else:
			raise Exception(f'Attempt to access invalid plane: Plane {currentPlane}; Direction {currentDirection}')

		# Convert the local position to world position in the next plane
		next = local_to_world(nextPlane, local.x, local.y)
	else:
		nextDirection = currentDirection

	return (next, nextDirection)

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

## Read input
with open('day22_input.txt') as file:
	lines = [ line.rstrip('\n') for line in file ]
	
	gridLines = lines[:-2]
	instructionsLine = lines[-1]

## Parse grid
width = max([ len(line) for line in gridLines ])
height = len(gridLines)

# Make sure our grid is square
size = max(width, height)
planeSize = size // 4

width = size
height = size

for line in gridLines:
	# Add tiles to grid
	grid.extend([ tiles[c] for c in line ])

	# Pad until end of line
	grid.extend([ TILE_NULL ] * (width - len(line)))

# Pad extra empty lines
while len(grid) < size * size:
	grid.append(TILE_NULL)

## Parse instructions
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

# Initial setup
position = Point(grid.index(TILE_PATH), 0)
direction = DR

## Simulate instructions
for instruction in instructions:
	if isinstance(instruction, int):
		# Move ahead for N units
		for i in range(instruction):
			visitedLocations[position] = direction 
			#print_grid()

			# Determine at the next position
			next, nextDirection = next_position(position, direction)

			# If it is blocked, stop here
			if grid_get(next.x, next.y) == TILE_WALL:
				break

			# Move to the next position
			position = next
			direction = nextDirection

	else:
		# Rotate R (CW) or L (CCW)
		rotation = 1 if instruction == 'R' else -1
		direction = (direction + rotation + 4) % 4

	#print()

password = (position.y + 1) * 1000 + (position.x + 1) * 4 + direction
print(f'Password: {password}')