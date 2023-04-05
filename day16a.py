import re
import copy

totalTime = 30
startValve = 'AA'

def calculate_shortest_distance(src, dst, path = [ ]):
	if src == dst:
		return 0
	
	path = path + [ src ] 
	srcConnectingValves = valves[src]['connectingValves']
	dstConnectingValves = valves[dst]['connectingValves']

	# Check cached and direct connections
	if dst in srcConnectingValves:
		return srcConnectingValves[dst]
	
	if src in dstConnectingValves:
		return dstConnectingValves[src]
	
	# Otherwise enumerate connecting valves and try all routes
	shortestDistance = None
	for other, distance in srcConnectingValves.items():
		
		# Skip valves we already visited
		if distance != 1 or other in path:
			continue

		distanceThroughOther = calculate_shortest_distance(other, dst, path)

		# Skip if we can't reach (without backtracking)
		if distanceThroughOther == None:
			continue

		fullDistance = distance + distanceThroughOther
		shortestDistance = min(shortestDistance or fullDistance, fullDistance)

	# Store distance
	if shortestDistance != None:
		srcConnectingValves[dst] = shortestDistance
		dstConnectingValves[src] = shortestDistance

	return shortestDistance

# Read input file
with open("day16_input.txt") as file:
    lines = [ line.rstrip('\n') for line in file ]
    
# Parse valves from input lines
valves = { }
for line in lines:
	match = re.search('Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line)
        
	if not match:
		continue

	id = match.group(1)
	flowRate = int(match.group(2))
	connectingValves = [ valve.strip(' ') for valve in match.group(3).split(',') ]

	valves[id] = \
	{
		'flowRate': flowRate,
		'connectingValves': dict.fromkeys(connectingValves, 1)
	}

valveIDs = list(valves.keys())

# Calculate distance to other valves
print('Precalculating distances...')
for srcIndex, srcID in enumerate(valveIDs):
	srcConnectingValves = valves[srcID]['connectingValves']

	# Iterate over other valves
	for dstID in valveIDs[srcIndex + 1:]:

		# Skip direct connections
		if dstID in srcConnectingValves:
			continue

		# Calculate shortest distance (this method also stores the result)
		calculate_shortest_distance(srcID, dstID)

# Remove valves with zero flow rate, since we don't need them anymore
print('Pruning valves...')
for id in valveIDs:
	if id != startValve and valves[id]['flowRate'] == 0:
		del valves[id]

# Class to hold a potential solution state
class Solution:

	def __init__(self):
		pass

	@classmethod
	def initial_setup(cls):
		s = Solution()
		s.currentValveID = startValve
		s.remainingTime = totalTime
		s.releasedPressure = 0
		s.currentAction = None
		s.openValves = [ ]

		return s

	@classmethod
	def from_existing_solution(cls, solution, action):
		s = Solution()
		s.currentValveID = solution.currentValveID
		s.remainingTime = solution.remainingTime
		s.releasedPressure = solution.releasedPressure
		s.openValves = solution.openValves.copy()

		s.currentAction = action

		return s

	def release_pressure(self, ticks = 1):
		# Release pressure from open valves
		for id in self.openValves:
			self.releasedPressure += valves[id]['flowRate'] * ticks

	def select_best_action(self):
		currentValve = valves[self.currentValveID]
		potentialActions = [ ]

		# Consider all valves
		for id, valve in valves.items():

			# If it is already opened, skip it
			if id in self.openValves:
				continue

			flowRate = valve['flowRate']
			distance = currentValve['connectingValves'][id] if id != self.currentValveID else 0

			requiredTime = distance + 1

			# Skip if opening this would take all remaining time
			if requiredTime >= self.remainingTime:
				continue

			potentialActions.append(
			{
				'valveID': id,
				'duration': requiredTime,
				'value': (self.remainingTime - requiredTime) * flowRate,
			})

		# Possibly all valves are already open, or we cannot reach them in time
		if len(potentialActions) == 0:
			return None
		
		potentialActions.sort(reverse=True, key=lambda a: a['value'])

		# Calculate the true value of each action
		for action in potentialActions:
			s = Solution.from_existing_solution(self, action)

			action['value'] = s.calculate_total_pressure()

			if self.remainingTime == totalTime:
				print(f'Start with {action["valveID"]}; Result: {action["value"]}')

		# Sort again
		potentialActions.sort(reverse=True, key=lambda a: a['value'])

		# Return the best action
		return potentialActions[0]

	def calculate_total_pressure(self):
		# Release pressure from open valves
		# Repeat this for each tick that our current action takes
		duration = self.currentAction['duration']

		self.release_pressure(duration)
		self.remainingTime -= duration

		# Finish current action
		valveID = self.currentAction['valveID']
		
		self.currentValveID = valveID
		self.openValves.append(valveID)
		
		self.currentAction = None

		# Check if we need to select a new action
		if self.remainingTime > 0:
			nextAction = self.select_best_action()

			# If there's an action to take, we already calculated the total value as well
			if nextAction != None:
				return nextAction['value']
		
			# Otherwise, finish the simulation
			self.release_pressure(self.remainingTime)
			self.remainingTime = 0

		return self.releasedPressure

# Simulate the optimal solution
solution = Solution.initial_setup()
action = solution.select_best_action()

print(f'Total pressure released: {action["value"]}')
