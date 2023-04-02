import re
from collections import namedtuple

Point = namedtuple('Point', 'x y')
Sensor = namedtuple('Sensor', 'position beacon')

def grid_index(position):
	return (position.y - minY) * width + (position.x - minX)

def grid_check(position):
	return position.x >= minX and position.x <= maxX and position.y >= minY and position.y <= maxY

def grid_set(position, value):
	grid[grid_index(position)] = value

def grid_get(position):
	return grid[grid_index(position)]

def distance(a, b):
	return abs(a.x - b.x) + abs(a.y - b.y)

def print_grid():
	output = ''
	for y in range(minY, maxY + 1):
		for x in range(minX, maxX + 1):
			output += grid_get(Point(x, y))
		
		output += '\n'

	print(output)

sensor = 'S'
beacon = 'B'
covered = '#'
unknown = '.'

with open("day15_example.txt") as file:
    lines = [ line.rstrip('\n') for line in file ]
    
# Parse sensors from input lines
sensors = [ ]
for line in lines:
	match = re.search('Sensor at x=(\d+), y=(\d+): closest beacon is at x=(\d+), y=(\d+)', line)
        
	if not match:
		continue

	sensors.append(Sensor(Point(int(match.group(1)), int(match.group(2))), Point(int(match.group(3)), int(match.group(4)))))

# Determine grid size
minX = None
minY = None
maxX = None
maxY = None	

for s in sensors:
	totalRange = distance(s.position, s.beacon)
	minX = min(minX or s.position.x, s.position.x - totalRange)
	minY = min(minY or s.position.y, s.position.y - totalRange)
	maxX = max(maxX or s.position.x, s.position.x + totalRange)
	maxY = max(maxY or s.position.y, s.position.y + totalRange)

width = maxX - minX + 1
height = maxY - minY + 1

print(f'Grid range: ({minX};{minY}) to ({maxX};{maxY})')
print(f'Creating grid of {width}x{height}...')

# Create grid
grid = [ ]
for y in range(minY, maxY + 1):
	for x in range(minX, maxX + 1):
		grid.append(unknown)

# Add sensors, beacon and covered range to grid
for s in sensors:
	grid_set(s.position, sensor)
	grid_set(s.beacon, beacon)
	
	# Write sensor covered area
	totalRange = distance(s.position, s.beacon)
	for dy in range(-totalRange, totalRange + 1):
		xRange = totalRange - abs(dy)

		for dx in range(-xRange, xRange + 1):
			position = Point(s.position.x + dx, s.position.y + dy)

			if not grid_check(position):
				continue

			if grid_get(position) != unknown:
				continue

			grid_set(position, covered)

# Count covered positions at target row
targetY = 10
coveredPositions = 0
for x in range(minX, maxX + 1):
	if grid_get(Point(x, targetY)) == covered:
		coveredPositions += 1

# Print output
print_grid()

print(f'Covered positions: {coveredPositions}')