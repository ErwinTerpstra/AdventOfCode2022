import sys

class Rock:
	def __init__(self):
		self.width = 0
		self.height = 0

		self.rows = [ ]

	def add_row(self, line):
		self.rows.append([ char == '#' for char in line ])

		self.width = max(self.width, len(line))
		self.height = len(self.rows)

	def get(self, x, y):
		return self.rows[y][x]

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
		
		return self.cells[y * self.width + x]

	def set(self, x, y):
		# Make sure the grid is large enough
		while y >= self.height:
			self.add_row()

		# Mark the grid cell as "blocked"
		self.cells[y * self.width + x] = True

	def print(self):
		for y in range(self.height):
			row = '|'

			for x in range(self.width):
				row += '#' if self.get(x, self.height - y - 1) else '.'

			row += '|'

			print(row)

		print('+-------+')

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
		rock = Rock()
		rocks.append(rock)

		for line in reversed(rockLines):
			rock.add_row(line)
		
	
# Parse input
with open("day17_example.txt") as file:
	jets = [ -1 if jet == '<' else 1 for jet in file.readline().rstrip('\n') ]

print(f'{len(jets)} jets')

# Simulate rocks
grid = Grid()
jetIdx = 0

rockCount = int(sys.argv[1]) if len(sys.argv) > 1 else 5

for rockIdx in range(rockCount):
	# Select a new rock
	# We don't actually add it to the grid until it's settled
	rock = rocks[rockIdx % len(rocks)]
	rockX = 2
	rockY = grid.height + 3

	while True:
		# Apply jet pushing
		jetDirection = jets[jetIdx % len(jets)]

		# Check if we can move the rock left/right
		isBlocked = False
		for ry in range(rock.height):
			rx = rock.get_base_width(ry, jetDirection)

			if grid.get(rockX + rx + jetDirection, rockY + ry):
				isBlocked = True
				break

		# Move the rock if not blocked
		if not isBlocked:
			rockX += jetDirection

		jetIdx += 1

		# Check if we can move the rock down
		isBlocked = False
		for rx in range(rock.width):
			ry = rock.get_base_height(rx)

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

	if rockIdx % 10000 == 0:
		print(f'Finished rock {rockIdx}')

print(f'Grid height: {grid.height}')