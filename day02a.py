import math

with open("day02_input.txt") as file:
	games = [ line.rstrip('\n').split(' ') for line in file ]
	totalScore = 0

	for game in games:
		action = ord(game[0]) - ord('A')
		reaction = ord(game[1]) - ord('X')

		n = reaction - action
		result = (((abs(n) + 1) % 3) - 1) * math.copysign(1, n)
		score = (result + 1) * 3 + (reaction + 1)

		totalScore += score

	print(f'Total score: {totalScore}')