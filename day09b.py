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
	
	knots = [ ]

	for i in range(0, 10):
		knots.append({ 'x': 0, 'y': 0 })

	tailPositions = { }
	
	tailPositions[tail_key(knots[-1])] = 1

	for line in lines:
		( direction, distance ) = line.split(' ')
		offset = directions[direction]

		for i in range(0, int(distance)):
			knots[0]['x'] += offset['x']
			knots[0]['y'] += offset['y']

			for k in range(1, len(knots)):
				deltaX = knots[k - 1]['x'] - knots[k]['x']
				deltaY = knots[k - 1]['y'] - knots[k]['y']

				if abs(deltaX) > 1 or abs(deltaY) > 1:
					knots[k]['x'] += sign(deltaX)
					knots[k]['y'] += sign(deltaY)

			tailKey = tail_key(knots[-1])
			tailPositions[tailKey] = tailPositions.get(tailKey, 0) + 1

	print(len(tailPositions))