from collections import namedtuple

Point = namedtuple('Point', 'x y z')
neighbours = \
[   
	# Front/Back
	Point( 0,  0, -1),
	Point( 0,  0,  1),
	
	# Left/Right
	Point(-1,  0,  0),
	Point( 1,  0,  0),
	
	# Up/Down
	Point( 0, -1, 0),
	Point( 0,  1, 0),
]

with open("day18_input.txt") as file:
	voxels = [ Point(*[int(value) for value in line.rstrip('\n').split(',')]) for line in file ]
	
grid = set(voxels)
air = set()

# Determine limits of grid
minBound = voxels[0]
maxBound = voxels[0]

for voxel in voxels:
	minBound = Point(min(minBound.x, voxel.x), min(minBound.y, voxel.y), min(minBound.z, voxel.z))
	maxBound = Point(max(maxBound.x, voxel.x), max(maxBound.y, voxel.y), max(maxBound.z, voxel.z))

minBound = Point(minBound.x - 1, minBound.y - 1, minBound.z - 1)
maxBound = Point(maxBound.x + 1, maxBound.y + 1, maxBound.z + 1)

# "Flood fill" from an empty position
openList = [ minBound ]
while len(openList) > 0:
	position = openList.pop()

	# Mark position as "empty air"
	air.add(position)

	# Add neighbours to open list
	for offset in neighbours:
		neighbour = Point(position.x + offset.x, position.y + offset.y, position.z + offset.z)

		# Limit to grid limits
		if neighbour.x < minBound.x or neighbour.y < minBound.y or neighbour.z < minBound.z \
			or neighbour.x > maxBound.x or neighbour.y > maxBound.y or neighbour.z > maxBound.z:
			continue

		# Skip positions covered by magma or already known to be empty
		if neighbour in voxels or neighbour in air:
			continue

		# Skip duplicate positions
		if neighbour in openList:
			continue
		
		openList.append(neighbour)

# Calculate surface
totalSurface = 0
for voxel in voxels:
	
	for offset in neighbours:
		neighbour = Point(voxel.x + offset.x, voxel.y + offset.y, voxel.z + offset.z)
		
		if neighbour in air:
			totalSurface += 1
		
print(f'Total surface: {totalSurface}') 