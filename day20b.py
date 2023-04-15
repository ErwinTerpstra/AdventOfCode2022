def sign(x):
	return (x > 0) - (x < 0)

def list_move(list, index, offset):
	if offset == 0:
		return

	value = list[index]
	length = len(list)
	lastIndex = length - 1

	# Determine start and end, make sure both are positiv
	start = index
	end = index + offset

	# Manual wrapping instead of modulo since we need length - 1
	# This is because inserting in the first slot and the last slot result in the same order
	if end < 0:
		n = -end // lastIndex
		end += (n + 1) * lastIndex

	if end >= length:
		n = (end - length) // lastIndex
		end -= (n + 1) * lastIndex

	# Determine which direction to shift
	direction = sign(end - start)

	# Shift the list
	for i in range(start, end, direction):
		list[i] = list[i + direction]

	# Reinsert the value
	list[end] = value

# Put back together an ordered list of values from the index list
def restore_list():
	return [ values[index] for index in indices]

###

# Read input
decryptionKey = 811589153
with open('day20_input.txt') as file:
	values = [ int(line) * decryptionKey for line in file ]
	
indices = list(range(len(values)))

# Move all numbers
for i in range(10):
	for index in range(len(indices)):
		position = indices.index(index)
		value = values[index]
		
		list_move(indices, position, value)

	print(f'Iteration #{i + 1} done!')

# Calculate result
result = restore_list()
zeroIndex = result.index(0)

a = result[(zeroIndex + 1000) % len(result)]
b = result[(zeroIndex + 2000) % len(result)]
c = result[(zeroIndex + 3000) % len(result)]

print(a + b + c)