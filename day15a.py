import re
from collections import namedtuple

Point = namedtuple('Point', 'x y')
Sensor = namedtuple('Sensor', 'position beacon')

targetY = 2000000
sensor = 'S'
beacon = 'B'
covered = '#'
unknown = '.'

def distance(a, b):
	return abs(a.x - b.x) + abs(a.y - b.y)

with open("day15_input.txt") as file:
    lines = [ line.rstrip('\n') for line in file ]
    
# Parse sensors from input lines
sensors = [ ]
for line in lines:
	match = re.search('Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)', line)
        
	if not match:
		continue

	sensors.append(Sensor(Point(int(match.group(1)), int(match.group(2))), Point(int(match.group(3)), int(match.group(4)))))

# Determine grid size
minX = None
minY = None
maxX = None
maxY = None	

for s in sensors:
	maxDistance = distance(s.position, s.beacon)
	minX = min(minX or s.position.x, s.position.x - maxDistance)
	minY = min(minY or s.position.y, s.position.y - maxDistance)
	maxX = max(maxX or s.position.x, s.position.x + maxDistance)
	maxY = max(maxY or s.position.y, s.position.y + maxDistance)

width = maxX - minX + 1
height = maxY - minY + 1

print(f'Grid range: ({minX};{minY}) to ({maxX};{maxY})')

# Create array for our target row
row = [ ]
for x in range(minX, maxX + 1):
	row.append(unknown)

# Add sensors, beacon and covered range to grid
for s in sensors:

	# Write sensor
	if s.position.y == targetY:
		row[s.position.x - minX] = sensor

	# Write beacon
	if s.beacon.y == targetY:
		row[s.beacon.x - minX] = beacon

	# Write sensor covered area
	maxDistance = distance(s.position, s.beacon)
	xRange = maxDistance - abs(s.position.y - targetY)

	if xRange <= 0:
		continue

	for x in range(s.position.x - xRange, s.position.x + xRange + 1):
		i = x - minX

		if row[i] == unknown:
			row[i] = covered

# Count covered positions at target row
coveredPositions = 0
for cell in row:
	if cell == covered or cell == sensor:
		coveredPositions += 1

print(f'Covered positions: {coveredPositions}')