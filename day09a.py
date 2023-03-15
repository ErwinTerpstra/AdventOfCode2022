directions = \
{
	'U': { 'x':  0, 'y':  1 },
	'D': { 'x':  0, 'y': -1 },
	'L': { 'x': -1, 'y':  0 },
	'R': { 'x':  1, 'y':  0 },
}

def tail_key(tail):
	return f"{tail['x']}-{tail['y']}"

def sign(a):
    return (a > 0) - (a < 0)

with open("day09_input.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]
	
	head = { 'x': 0, 'y': 0 }
	tail = { 'x': 0, 'y': 0 }

	tailPositions = { }
	
	tailPositions[tail_key(tail)] = 1

	for line in lines:
		( direction, distance ) = line.split(' ')
		offset = directions[direction]

		for i in range(0, int(distance)):
			head['x'] += offset['x']
			head['y'] += offset['y']

			deltaX = head['x'] - tail['x']
			deltaY = head['y'] - tail['y']

			if abs(deltaX) > 1 or abs(deltaY) > 1:
				tail['x'] += sign(deltaX)
				tail['y'] += sign(deltaY)

			tailKey = tail_key(tail)
			tailPositions[tailKey] = tailPositions.get(tailKey, 0) + 1

	print(len(tailPositions))