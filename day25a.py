SNAFU_DIGITS = \
{
	'0': 0,
	'1': 1,
	'2': 2,
	
	'-': -1,
	'=': -2
}

SNAFU_DIGITS_INVERSE = \
{
	-2: '=',
	-1: '-',
	 0: '0',
	 1: '1',
	 2: '2',
}

def snafu_to_dec(snafu):
	value = 0
	base = 1

	for c in reversed(snafu):
		digit = SNAFU_DIGITS[c]

		value += digit * base
		base *= 5

	return value

def dec_to_snaf(dec):
	snafu = ''
	base = 1
	carry = 0

	while dec > 0:
		value = (dec % 5) + carry
		dec = dec // 5
		
		if value > 2:
			value -= 5
			carry = 1
		else:
			carry = 0

		snafu = SNAFU_DIGITS_INVERSE[value] + snafu

	return snafu

with open('day25_input.txt') as file:
	lines = [ line.rstrip('\n') for line in file ]
	
sum = 0
for line in lines:
	value = snafu_to_dec(line)

	print(f'{line.ljust(20)} is {value}')
	
	sum += value
	
print()
print(f'Fuel requirement: {sum}. SNAFU: {dec_to_snaf(sum)}')