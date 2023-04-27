from collections import namedtuple
from dataclasses import dataclass

@dataclass
class Point:
	x: int
	y: int

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	
	def __hash__(self) -> int:
		return (self.y << 10) | self.x

	def __eq__(self, other: object) -> bool:
		return self.x == other.x and self.y == other.y
		
	
@dataclass
class Blizzard:
	position: Point
	direction: int

@dataclass
class State:
	tick: int
	position: Point

	@classmethod
	def hash(cls, state) -> int:
		return (hash(state.position) << 12) | state.tick

DIRECTION_CHARACTERS = \
{
	'>': 0,
	'v': 1,
	'<': 2,
	'^': 3
}

DIRECTION_OFFSETS = \
[
	Point( 1,  0),
	Point( 0,  1),
	Point(-1,  0),
	Point( 0, -1),

	Point( 0,  0), # "Fake" direction to make considering not moving easier
]

blizzards = [ ]

with open('day24_input.txt') as file:
	lines = [ line.rstrip('\n') for line in file ]

# Width and height without borders
height = len(lines) - 2
width = len(lines[0]) - 2
size = width * height

def in_grid(x, y):
	return x >= 0 and x < width and y >= 0 and y < height

# Read all blizzards from the input data
for y in range(0, height):
	for x in range(0, width):
		character = lines[y + 1][x + 1]

		if character in DIRECTION_CHARACTERS:
			position = Point(x, y)
			direction = DIRECTION_CHARACTERS[character]

			blizzards.append(Blizzard(position, direction))
		elif character != '.':
			print(f'Warning! Encountered unknown character "{character}"')

# Determine the tick interval after which all blizzards have cycled back to the same position
cycleInterval = width
while cycleInterval % height != 0:
	cycleInterval += width

print(f'Precalculating {cycleInterval} states...')
print()

# Precalculate blizzard positions for each tick in the cycle interval
# This array will hold rasterized grid states for each tick
blizzardStates = [ ]

# Helper functions to set or get a blizzard state at a certain position
def blizzard_set(tick, x, y):
	blizzardStates[tick % cycleInterval][y * width + x] = True

def blizzard_get(tick, x, y):
	return blizzardStates[tick % cycleInterval][y * width + x]

def blizzard_print(tick):

	print('#' * (width + 2))

	for y in range(height):
		line = '#'
		
		for x in range(width):
			line += '*' if blizzard_get(tick, x, y) else '.'

		line += '#'

		print(line)
			
	print('#' * (width + 2))

# For each tick in our cycle, calculate blizzard positions
for i in range(cycleInterval):
	blizzardStates.append([False] * size)

	for blizzard in blizzards:
		offset = DIRECTION_OFFSETS[blizzard.direction]
		
		blizzardX = ((blizzard.position.x + offset.x * i) + width) % width
		blizzardY = ((blizzard.position.y + offset.y * i) + height) % height

		blizzard_set(i, blizzardX, blizzardY)

	print(f'Tick #{i} done')
	#blizzard_print(i)
	#print()

initialState = State(0, Point(0, -1))
target = Point(width - 1, height)

openList = [ initialState ]
closedList = set()
fastestToTarget = -1
visitedStates = 0
highestTick = 0

while len(openList) > 0:
	state = openList.pop()
	highestTick = max(state.tick, highestTick)

	# Consider all neighbour directions
	for offset in DIRECTION_OFFSETS:
		newTick = state.tick + 1
		newPosition = state.position + offset

		# Skip states that won't result in a faster route
		if fastestToTarget != -1 and newTick >= fastestToTarget:
			continue

		# Check if this position reaches the target
		if newPosition == target:
			# Check if it's the newest fastest route
			if fastestToTarget == -1 or newTick < fastestToTarget:
				fastestToTarget = newTick

			continue

		# Skip outside of grid
		if not in_grid(newPosition.x, newPosition.y):
			continue

		# Skip states that would end in a blizzard
		if blizzard_get(newTick, newPosition.x, newPosition.y):
			continue

		# Create new state
		newState = State(newTick, newPosition)
		newStateHash = State.hash(newState)

		# Verify if we haven't already visited this state
		if newStateHash in closedList:
			continue

		openList.insert(0, newState)
		closedList.add(newStateHash)

	visitedStates += 1

	if visitedStates % 1000 == 0:
		print(f'Visited {visitedStates} states. Fastest time to target: {fastestToTarget}; Highest tick: {highestTick}')

print(f'Fastest time to target: {fastestToTarget}')