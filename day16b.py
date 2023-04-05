import re
import copy

totalTime = 26
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

valveIDs = list(valves.keys())

# Class to hold an action in progress
class Action:

	def __init__(self, valveID, duration):
		self.valveID = valveID
		self.duration = duration

	def copy(self):
		return Action(self.valveID, self.duration)
	
	def __str__(self):
		return f'{self.valveID} ({self.duration})'

# Class to represent an actor that moves through tunnels opens valves
class Actor:

	def __init__(self, valveID):
		self.valveID = valveID
		self.action = None

	def copy(self, action = None):
		a = Actor(self.valveID)

		if action != None:
			a.action = action
		elif self.action != None:
			a.action = self.action.copy()

		return a

def release_pressure(openValves, ticks = 1):
	releasedPressure = 0

	# Release pressure from open valves
	for id in openValves:
		releasedPressure += valves[id]['flowRate'] * ticks

	return releasedPressure

def simulate_solution(remainingTime, actors, openValves = [ ], depth = 0):
	# If there are no active actors left, simulate remaining time
	if len(actors) == 0:
		return release_pressure(openValves, remainingTime)

	# Attempt to find the first actor without an action
	currentActor = next((actor for actor in actors if actor.action == None), None)

	# Otherwise, find the actor with lowest duration
	if currentActor == None:
		currentActor = min(actors, key=lambda a: a.action.duration)

	# Check if the current actor has an action we want to finish first
	if currentActor.action != None:
		valveID = currentActor.action.valveID
		duration = currentActor.action.duration

		# Calculate pressure released until action has finished
		currentReleasedPressure = release_pressure(openValves, duration)

		# Finish the actor's action
		currentActor.valveID = valveID
		currentActor.action = None
		
		openValves.append(valveID)

		# Subtract the passed time from our clock 
		remainingTime -= duration

		# Subtract the passed time from other actor's waiting times
		for actor in actors:
			if actor.action != None:
				actor.action.duration -= duration
	else:
		currentReleasedPressure = 0
			
	# Consider all valves
	connectingValves = valves[currentActor.valveID]['connectingValves']
	futureReleasedPressure = None
	for valveID in valveIDs:
		if valves[valveID]['flowRate'] == 0:
			continue

		# If it is already opened, skip it
		if valveID in openValves:
			continue

		# Skip actions that are already being taken by another actor
		if any(actor.action != None and actor.action.valveID == valveID for actor in actors):
			continue

		distance = connectingValves[valveID] if valveID != currentActor.valveID else 0
		requiredTime = distance + 1

		# Skip if opening this would take all remaining time
		if requiredTime >= remainingTime:
			continue
		
		# Create a data structure holding the action
		action = Action(valveID, requiredTime)

		# Copy the list of actors, assigning the action to the current actor
		newActors = [ actor.copy(action if actor == currentActor else None) for actor in actors ]

	 	# Recursively calulate the max future released pressure
		releasedPressure = simulate_solution(remainingTime, newActors, openValves.copy(), depth + 1)

		# Check if this is higher than our current max
		futureReleasedPressure = max(releasedPressure, futureReleasedPressure or 0)

		if depth == 0:
			print(f'Start with {valveID}; Result: {releasedPressure}')

	# If no other actions are possible
	if futureReleasedPressure == None:
		# Continue simulating without this actor, to give other actors the chance to finish their actions
		actors.remove(currentActor)
		futureReleasedPressure = simulate_solution(remainingTime, actors, openValves, depth + 1)

	# Return total pressure
	return currentReleasedPressure + futureReleasedPressure

# Simulate the optimal solution
print('Calculating solution...')

totalReleasedPressure = simulate_solution(totalTime, [ Actor(startValve), Actor(startValve) ])

print(f'Total pressure released: {totalReleasedPressure}')
