def sign(x):
	return (x > 0) - (x < 0)

def list_move(list, index, offset):
	if offset == 0:
		#print('0 doesn\'t move')
		return

	value = list[index]
	length = len(list)

	# Determine start and end, make sure both are positiv
	start = index
	end = index + offset

	# Manual wrapping instead of modulo since we need -1/+1
	# This is because inserting in the first slot and the last slot result in the same order
	while end < 0:
		end = length + end - 1
	
	while end >= length:
		end = (end - length + 1)

	# Determine which direction to shift
	direction = sign(end - start)

	# print(f'{offset} from {start} to {end}')

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
with open('day20_input.txt') as file:
	values = [ int(line) for line in file ]
	
indices = list(range(len(values)))

# Print initial state
# print(restore_list())
# print()

# Move all numbers
for index in range(len(indices)):
	position = indices.index(index)
	value = values[index]
	
	list_move(indices, position, value)

	# print(restore_list())
	# print()

# Calculate result
result = restore_list()
zeroIndex = result.index(0)

a = result[(zeroIndex + 1000) % len(result)]
b = result[(zeroIndex + 2000) % len(result)]
c = result[(zeroIndex + 3000) % len(result)]

print(a + b + c)