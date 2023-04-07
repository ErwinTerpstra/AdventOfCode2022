import sys

from timeit import default_timer as timer
from datetime import timedelta

class Rock:
	def __init__(self, width):
		self.width = width
		self.height = 0

		self.offset_horizontal = { -1: [ ], 1: [ ] }
		self.offset_bottom = [ ]

		self.cells = [ ]

	def add_row(self, line):
		self.cells.extend([ char == '#' for char in line ])

		self.height += 1

	def get(self, x, y):
		return self.cells[y * self.width + x]

	def get_base_width(self, y, side):
		for x in range(self.width):
			lx = x if side == -1 else self.width - x - 1

			if self.get(lx, y):
				return lx

		raise Exception('Error! Empty row in rock')

	def get_base_height(self, x):
		for y in range(self.height):
			if self.get(x, y):
				return y
			
		raise Exception('Error! Empty column in rock')			
	
	def precalculate(self):
		for y in range(self.height):
			self.offset_horizontal[-1].append(self.get_base_width(y, -1))
			self.offset_horizontal[ 1].append(self.get_base_width(y,  1))

		for x in range(self.width):
			self.offset_bottom.append(self.get_base_height(x))

	
	def print(self):
		for y in range(self.height):
			row = ''
			
			for x in range(self.width):
				row += '#' if self.get(x, self.height - y - 1) else '.'

			print(row)

class Grid:
	def __init__(self):
		self.cells = [ ]

		self.width = 7

		self.startY = 0
		self.height = 0

	def add_row(self):
		for x in range(self.width):
			self.cells.append(False)

		self.height += 1

	def get(self, x, y):
		if y < 0:
			return True
		
		if x < 0 or x >= self.width:
			return True
		
		if y >= self.height:
			return False
		
		return self.cells[(y - self.startY) * self.width + x]

	def set(self, x, y):
		# Make sure the grid is large enough
		while y >= self.height:
			self.add_row()

		# Mark the grid cell as "blocked"
		self.cells[(y - self.startY) * self.width + x] = True

	def prune(self):
		if self.height < 2:
			return
		
		highest = self.height

		for x in range(self.width):
			for y in range(self.height - 1, self.startY - 1, -1):
				if self.get(x, y):
					break

			highest = min(highest, y)				

		# Prune from startY to highest - 1
		newStartY = highest
		prunedRows = max(newStartY - self.startY, 0)

		if prunedRows > 0:
			#print(f'Pruning {prunedRows} rows')

			self.startY = newStartY
			self.cells = self.cells[prunedRows * self.width:]


	def print(self):
		for y in range(self.height - 1, self.startY - 1, -1):
			row = '|'

			for x in range(self.width):
				row += '#' if self.get(x, y) else '.'

			row += '|'

			print(row)

		print(f'+-------+ {self.startY}')

	def __hash__(self):
		result = 0

		for n in range(len(self.cells)):
			result |= int(self.cells[n]) << n

		return result

class Cycle:
	def __init__(self, iteration, height):
		self.iteration = iteration
		self.height = height

def group(sequence, separator):
	g = [ ]

	for element in sequence:
		if element == separator:
			yield g

			g = [ ]
		else:
			g.append(element)

	yield g

# Parse rocks
rocks = [ ]
with open("day17_rocks.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]

	rock = None
	for rockLines in group(lines, ''):
		rock = Rock(len(rockLines[0]))

		for line in reversed(rockLines):
			rock.add_row(line)

		rock.precalculate()
		rocks.append(rock)
		
	
# Parse input
with open("day17_input.txt") as file:
	jets = [ -1 if jet == '<' else 1 for jet in file.readline().rstrip('\n') ]


# Determine cycle parameters
rockCount = len(rocks)
jetCount = len(jets)

print(f'{rockCount} rocks; {jetCount} jets')
print('Determining cycle interval...')

cycleInterval = jetCount
while cycleInterval % rockCount != 0:
	cycleInterval += jetCount

print(f'Cycle interval: {cycleInterval}')

# Simulate rocks
grid = Grid()

rockIdx = 0
jetIdx = 0

iteration = 0
iterationCount = int(sys.argv[1]) if len(sys.argv) > 1 else 5
lastTime = timer()
states = { }

while iteration < iterationCount:
	# Select a new rock
	# We don't actually add it to the grid until it's settled
	rock = rocks[rockIdx]
	rockIdx = (rockIdx + 1) % rockCount

	rockX = 2
	rockY = grid.height + 3

	while True:
		# Apply jet pushing
		jetDirection = jets[jetIdx]
		jetIdx = (jetIdx + 1) % jetCount

		# Check if we can move the rock left/right
		isBlocked = False
		offsets = rock.offset_horizontal[jetDirection]
		for ry in range(rock.height):
			rx = offsets[ry]

			if grid.get(rockX + rx + jetDirection, rockY + ry):
				isBlocked = True
				break

		# Move the rock if not blocked
		if not isBlocked:
			rockX += jetDirection

		# Check if we can move the rock down
		isBlocked = False
		for rx in range(rock.width):
			ry = rock.offset_bottom[rx]

			if grid.get(rockX + rx, rockY + ry - 1):
				isBlocked = True
				break

		if isBlocked:
			break

		rockY -= 1

	# Add the rock to the grid
	for ry in range(rock.height):
		for rx in range(rock.width):
			if rock.get(rx, ry):
				grid.set(rockX + rx, rockY + ry)

	# Prune unreachable rows from grid
	if rockIdx == 0:
		grid.prune()

	# Store hash in states dict, compare to previous found
	if iteration % cycleInterval == 0:
		stateHash = hash(grid);
		if stateHash in states:
			previousIteration = states.get(stateHash)
			cycleLength = iteration - previousIteration.iteration
			deltaHeight = grid.height - previousIteration.height

			print(f'Detected cycle at iteration {iteration}; Cycle length: {cycleLength}')

			# Calculate how often we still want to repeate this cycle
			remainingIterations = iterationCount - iteration - 1
			cycles = remainingIterations // cycleLength

			# Simulate N cycles
			iteration += cycleLength * cycles

			grid.startY += deltaHeight * cycles
			grid.height += deltaHeight * cycles

			# Clear states since we don't want to recognize all subsequent cycle steps
			states.clear()
		else:
			states[stateHash] = Cycle(iteration, grid.height)

	# Logging and timing
	if iteration % 100000 == 0:
		now = timer()
		print(f'Finished iteration {iteration} in {timedelta(seconds=now - lastTime)}')
		lastTime = now

	iteration += 1

print(f'Grid height: {grid.height}')