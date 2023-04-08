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
totalSurface = 0

for voxel in voxels:
	surface = len(neighbours)
	
	for offset in neighbours:
		neighbour = Point(voxel.x + offset.x, voxel.y + offset.y, voxel.z + offset.z)
		
		if neighbour in grid:
			surface -= 1
		
	totalSurface += surface
		
print(f'Total surface: {totalSurface}') 