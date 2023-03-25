import json
import functools

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

divider0 = [[2]]
divider1 = [[6]]

elements = [ divider0, divider1 ]

with open("day13_input.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]
	
	# Load all non-empty lines as json
	for line in lines:
		if len(line) > 0:
			elements.append(json.loads(line))

elements.sort(key=functools.cmp_to_key(compare), reverse=True)

index0 = elements.index(divider0) + 1
index1 = elements.index(divider1) + 1

print(f'Decoder key: {index0 * index1}')