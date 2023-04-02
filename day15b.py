import re
from collections import namedtuple

Point = namedtuple('Point', 'x y')
Segment = namedtuple('Segment', 'start end')
Sensor = namedtuple('Sensor', 'position beacon maxRange')

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

	position = Point(int(match.group(1)), int(match.group(2)))
	beacon = Point(int(match.group(3)), int(match.group(4)))
	maxRange = distance(position, beacon)
	sensors.append(Sensor(position, beacon, maxRange))

# Sort sensors by Y position
sensors.sort(key=lambda s: s.position.y)

minX = 0
minY = 0
maxX = 4000000
maxY = 4000000

width = maxX - minX + 1
height = maxY - minY + 1
foundBeacon = False

segments = [ ]
for y in range(minY, maxY + 1):
	# Setup empty list of open ranges
	segments.clear()
	segments.append(Segment(minX, maxX))
	
	# Add all sensor ranges to this row
	for s in sensors:
		# Determine sensor covered area
		xRange = s.maxRange - abs(y - s.position.y)

		if xRange < 0:
			continue

		startX = max(s.position.x - xRange, minX)
		endX = min(s.position.x + xRange, maxX)

		# Update our segments list with this sensor
		i = 0
		while i < len(segments):
			segment = segments[i]

			# Fully before segment, no more segments viable
			if endX < segment.start:
				break
			
			# Fully after segment, find next
			if startX > segment.end:
				i += 1
				continue

			# Overlapping start of start
			# Decrease size of segment
			if startX < segment.start and endX < segment.end:
				segments[i] = Segment(endX + 1, segment.end)
				break

			# Overlapping end of segment
			# Decrease size of segment
			if startX > segment.start and endX > segment.end:
				segments[i] = Segment(segment.start, startX - 1)
				i += 1
				continue

			# Segment fully contained in sensor, remove it entirely
			if startX <= segment.start and endX >= segment.end:
				del segments[i]
				continue

			# Sensor fully contained in segment, split the segment
			left = Segment(segment.start, startX - 1)
			right = Segment(endX + 1, segment.end)

			del segments[i]

			if left.start <= left.end:
				segments.insert(i, left)
				i += 1

			if right.start <= right.end:
				segments.insert(i, right)
				i += 1

			break

		# If all positions are filled, we can continue to the next row
		if len(segments) == 0:
			break

	# Check if there is only one free segment
	if len(segments) > 0:
		if len(segments) == 1 and segments[0].start == segments[0].end:
			# Calculate tuning frequency (puzzle solution)
			x = segments[0].start
			tuningFrequency = (x * 4000000) + y
			foundBeacon = True

			print(f'Beacon discovered at ({x};{y}) with tuning frequency: {tuningFrequency}')
			break
		else:
			print(f'Error! Multiple possible positions at row {y}')
			print(segments)
			break

	if y % 1000 == 0:
		print(f'Current row: {y}')

if not foundBeacon:
	print('Error! No possible beacon position found.')