import json

def sign(x):
	return (x > 0) - (x < 0)

def compare(a, b):

	aLeaf = isinstance(a, int)
	bLeaf = isinstance(b, int)

	# First, check if both are integers
	if aLeaf and bLeaf:
		return sign(b - a)
	
	# Otherwise, make sure both are lists
	if aLeaf:
		a = [ a ]

	if bLeaf:
		b = [ b ]

	lenA = len(a)
	lenB = len(b)

	for i in range(min(lenA, lenB)):
		result = compare(a[i], b[i])

		if result != 0:
			return result

	return sign(lenB - lenA)

with open("day13_input.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]

currentPair = 1
sum = 0

while len(lines) > 1:
	# Get next two lines as JSON
	a = json.loads(lines.pop(0))
	b = json.loads(lines.pop(0))

	if compare(a, b) > 0:
		sum += currentPair

	# Consume trailing empty lines
	while len(lines) > 0 and len(lines[0]) == 0:
		lines.pop(0)

	currentPair += 1

print(f'Sum of pair indices: {sum}')