from collections import namedtuple
from sys import maxsize

Point = namedtuple('Point', 'x y')
Direction = namedtuple('Direction', 'offset neighbours')

class Elf:
	def __init__(self, position):
		self.position = position
		self.action = None
		
def build_elf_map():
	elfMap.clear()

	for elf in elves:
		elfMap[elf.position] = elf

def build_action_map():	
	actionMap.clear()

	for elf in elves:
		if elf.action == None:
			continue

		actionMap[elf.action] = actionMap.get(elf.action, 0) + 1

def count_valid_actions():
	return sum(n == 1 for pos, n in actionMap.items())

def select_actions():
	# Select an action for each elve
	for elf in elves:
		# Reset this elf's action
		elf.action = None

		# Collect neighbours for this elf
		neighbourBuffer.clear()
		for neighbourOffset in neighbours:
			neighbourPosition = Point(elf.position.x + neighbourOffset.x, elf.position.y + neighbourOffset.y)
			neighbourBuffer.append(elfMap.get(neighbourPosition, None))

		# If this elf has no neighbours, it does nothing
		neighbourCount = sum(x != None for x in neighbourBuffer)
		if neighbourCount == 0:
			continue

		# Select an action for this elf
		# Consider all directions
		for directionIndex in range(4):
			direction = directions[(round + directionIndex) % len(directions)]

			# Consider all 3 tiles in this direction
			directionNeighbourCount = 0
			for neighbourIndex in direction.neighbours:
				directionNeighbourCount += neighbourBuffer[neighbourIndex] != None
			
			# If no elves are in any of those tiles, pick that direction
			if directionNeighbourCount == 0:
				elf.action = Point(elf.position.x + direction.offset.x, elf.position.y + direction.offset.y)
				break

def execute_actions():
	# Execute all scheduled actions
	for elf in elves:
		if elf.action == None:
			continue

		# Skip the action if multiple elves wanted to execute it
		if actionMap[elf.action] > 1:
			continue

		elf.position = elf.action

def determine_grid_range():
	minPosition = Point(maxsize, maxsize)
	maxPosition = Point(-maxsize, -maxsize)

	for elf in elves:
		minPosition = Point(min(minPosition.x, elf.position.x), min(minPosition.y, elf.position.y))
		maxPosition = Point(max(maxPosition.x, elf.position.x), max(maxPosition.y, elf.position.y))
		
	return (minPosition, maxPosition)

def print_grid():
	minPosition, maxPosition = determine_grid_range()
		
	for y in range(minPosition.y, maxPosition.y + 1):
		line = ''

		for x in range(minPosition.x, maxPosition.x + 1):
			position = Point(x, y)

			if position in elfMap:
				line += '#'
			else:
				line += '.'

		print(line)

def count_empty_tiles():
	minPosition, maxPosition = determine_grid_range()
	emptyTiles = 0
		
	for y in range(minPosition.y, maxPosition.y + 1):
		for x in range(minPosition.x, maxPosition.x + 1):
			position = Point(x, y)

			if not position in elfMap:
				emptyTiles += 1

	return emptyTiles

elves = [ ]
elfMap = { }
actionMap = { }

directions = \
[
	Direction(Point(0, -1), [ 0, 1, 2 ]),	# North
	Direction(Point(0,  1), [ 5, 6, 7 ]),	# South
	Direction(Point(-1, 0), [ 0, 3, 5 ]),	# West
	Direction(Point( 1, 0), [ 2, 4, 7 ]),	# East
]

neighbours = \
[
	Point(-1, -1),
	Point( 0, -1),
	Point( 1, -1),

	Point(-1,  0),
	Point( 1,  0),

	Point(-1,  1),
	Point( 0,  1),
	Point( 1,  1),
]

neighbourBuffer = [ ]
directionOffsets = [ ]

with open('day23_input.txt') as file:
	for y, line in enumerate(file):
		for x, char in enumerate(line):
			if char == '#':
				elf = Elf(Point(x, y))

				elves.append(elf)

# Prepare elf map
build_elf_map()

# Simulate N rounds
round = 0
while True:
	select_actions()
	build_action_map()

	if count_valid_actions() == 0:
		break

	execute_actions()
	build_elf_map()

	round += 1

	if round % 100 == 0:
		print(f'Round {round} finished')

print_grid()

print(f'No elf moved on round #{round + 1}')