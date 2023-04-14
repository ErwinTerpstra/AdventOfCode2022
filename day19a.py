import re
from collections import namedtuple

from timeit import default_timer as timer
from datetime import timedelta

RESOURCE_ORE 		= 0
RESOURCE_CLAY 		= 1
RESOURCE_OBSIDIAN 	= 2
RESOURCE_GEODE 		= 3

RESOURCE_NAME_ORE 		= 'ore'
RESOURCE_NAME_CLAY 		= 'clay'
RESOURCE_NAME_OBSIDIAN 	= 'obsidian'
RESOURCE_NAME_GEODE 	= 'geode'

RESOURCE_NAMES = \
[
	RESOURCE_NAME_ORE,
	RESOURCE_NAME_CLAY,
	RESOURCE_NAME_OBSIDIAN,
	RESOURCE_NAME_GEODE
]

TOTAL_TIME = 24

class State:
	def __init__(self, timeLeft = 0):
		self.timeLeft = timeLeft

		self.resources = [ 0, 0, 0, 0 ]
		self.robots = [ 0, 0, 0, 0 ]

	@classmethod
	def initial_state(cls):
		state = State(TOTAL_TIME)	
		state.robots[RESOURCE_ORE] = 1

		return state
	
	def __hash__(self):
		# Time left
		x = self.timeLeft

		# Resource amounts
		for i in range(4):
			x = (x << 8) | self.resources[i]

		# Robot amounts
		for i in range(4):
			x = (x << 5) | self.robots[i]

		return x
	
	def __eq__(self, other):
		if self is other:
			return True
		
		if not isinstance(other, State):
			return False
		
		return self.timeLeft == other.timeLeft and self.resources == other.resources and self.robots == other.robots

	def copy_from(self, other):
		self.timeLeft = other.timeLeft

		for resource in range(4):
			self.resources[resource] = other.resources[resource]
			self.robots[resource] = other.robots[resource]

	def step(self, factory, action):
		# Add robot resources
		for resource in range(4):
			self.resources[resource] += self.robots[resource]

		# Build robot
		if action != None:
			# Add robot to pool	
			self.robots[action] += 1

			# Subtract resources
			blueprint = factory.robots[action]
			for resource in range(4):
				self.resources[resource] -= blueprint.cost[resource]

		# Decrease time left
		self.timeLeft -= 1


	def select_actions(self, factory, actionBuffer):
		actionBuffer.clear()

		ore = self.resources[RESOURCE_ORE]
		clay = self.resources[RESOURCE_CLAY]
		obsidian = self.resources[RESOURCE_OBSIDIAN]

		oreBlueprint = factory.robots[RESOURCE_ORE]
		clayBlueprint = factory.robots[RESOURCE_CLAY]
		obsidianBlueprint = factory.robots[RESOURCE_OBSIDIAN]
		geodeBlueprint = factory.robots[RESOURCE_GEODE]

		oreBots = self.robots[RESOURCE_ORE]
		clayBots = self.robots[RESOURCE_CLAY]
		obsidianBots = self.robots[RESOURCE_OBSIDIAN]

		canBuildGeode = ore >= geodeBlueprint.cost[RESOURCE_ORE] and obsidian >= geodeBlueprint.cost[RESOURCE_OBSIDIAN]
		
		# Always build geode bots, if possible
		if canBuildGeode:
			actionBuffer.append(RESOURCE_GEODE)
			return
	
		if obsidianBots > 0:
			# Check what our bottleneck is in building geode bots
			timeUntilEnoughOre = geodeBlueprint.cost[RESOURCE_ORE] / oreBots 
			timeUntilEnoughObsidian = geodeBlueprint.cost[RESOURCE_OBSIDIAN] / obsidianBots

			prioritizeObsidian = timeUntilEnoughObsidian > timeUntilEnoughOre
		else:
			prioritizeObsidian = True

		if prioritizeObsidian:
			# Check what our bottleneck is in building obsidian robots
			if clayBots > 0:
				timeUntilEnoughOre = obsidianBlueprint.cost[RESOURCE_ORE] / oreBots
				timeUntilEnoughClay = obsidianBlueprint.cost[RESOURCE_CLAY] / clayBots

				prioritizeClay = timeUntilEnoughClay > timeUntilEnoughOre
			else:
				prioritizeClay = True
		else:
			prioritizeClay = False
		
		# Check which options are possible	
		canBuildOre = ore >= oreBlueprint.cost[RESOURCE_ORE] and oreBots <= factory.maxCost[RESOURCE_ORE]
		canBuildClay = ore >= clayBlueprint.cost[RESOURCE_ORE] and clayBots <= factory.maxCost[RESOURCE_CLAY]
		canBuildObsidian = ore >= obsidianBlueprint.cost[RESOURCE_ORE] and clay >= obsidianBlueprint.cost[RESOURCE_CLAY] and obsidianBots <= factory.maxCost[RESOURCE_OBSIDIAN]
		
		allowIdle = False
		
		if prioritizeObsidian:
			if canBuildObsidian:
				actionBuffer.append(RESOURCE_OBSIDIAN)
			else:
				allowIdle = True

		if prioritizeClay:
			if canBuildClay:
				actionBuffer.append(RESOURCE_CLAY)
			else:
				allowIdle = True
				
		if canBuildOre:
			actionBuffer.append(RESOURCE_ORE)
		else:
			allowIdle = True

		if allowIdle or len(actionBuffer) == 0:
			actionBuffer.append(None)

class FactoryBlueprint:
	def __init__(self, id):
		self.id = id
		self.robots = [ None, None, None, None ] 
		self.maxCost = [ 0, 0, 0, 0] 
	
	@classmethod
	def parse(cls, input):
		match = re.search('Blueprint (\d+): (.*\.) (.*\.) (.*\.) (.*\.)', input)

		if not match:
			return None
		
		blueprint = FactoryBlueprint(int(match.group(1)))

		for i in range(4):
			robot = RobotBlueprint.parse(match.group(2 + i))

			if not robot:
				continue

			blueprint.robots[robot.resource] = robot

			for resource in range(4):
				blueprint.maxCost[resource] = max(blueprint.maxCost[resource], robot.cost[resource])

		return blueprint
	
	def simulate(self):
		stateBuffer = [ ]
		actionBuffer = [ ]

		openList = [ State.initial_state() ]
		closedList = set()
		lastTime = timer()

		maxGeodes = 0

		while len(openList) > 0:
			state = openList.pop()
			state.select_actions(self, actionBuffer)

			stateHash = hash(state)
			closedList.add(stateHash)

			for action in actionBuffer:
				newState = stateBuffer.pop() if len(stateBuffer) > 0 else State()
				newState.copy_from(state)
				newState.step(self, action)

				# Check if the state isnt finished yet
				if newState.timeLeft > 0:
					newStateHash = hash(newState)

					if not newStateHash in closedList:
						openList.append(newState)
						continue

				# If this state is finished, check the resulting score
				maxGeodes = max(maxGeodes, newState.resources[RESOURCE_GEODE])

				# Add state to buffer for reuse
				stateBuffer.append(newState)

			# Add state to buffer for reuse
			stateBuffer.append(state)

			if len(closedList) % 100000 == 0:
				now = timer()
				print(f'State #{len(closedList)} done. Buffer size: {len(openList)}. Max geodes: {maxGeodes}. Delta time: {timedelta(seconds=now - lastTime)}');
		
				lastTime = now

		return maxGeodes

class RobotBlueprint:
	def __init__(self, resourceName):
		self.resource = RESOURCE_NAMES.index(resourceName)
		self.cost = [ 0, 0, 0, 0 ]
		
	def add_cost(self, resourceName, amount):
		self.cost[RESOURCE_NAMES.index(resourceName)] = amount

	@classmethod
	def parse(cls, input):
		match = re.search('Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?\.', input)

		if not match:
			return None

		groups = match.groups()		

		blueprint = RobotBlueprint(groups[0])

		blueprint.add_cost(groups[2], int(groups[1]))

		if groups[3] != None:
			blueprint.add_cost(groups[5], int(groups[4]))

		return blueprint
		
with open('day19_input.txt') as file:
	lines = [ line.rstrip('\n') for line in file ]
		
# Parse all possible factory blueprint
blueprints = [ ]
for line in lines:
	blueprint = FactoryBlueprint.parse(line)

	if not blueprint:
		continue

	blueprints.append(blueprint)

# Evaluate each blueprint
sum = 0
for blueprint in blueprints:
	geodes = blueprint.simulate()
	quality = blueprint.id * geodes

	sum += quality

	print(f'Blueprint #{blueprint.id}: {geodes} geodes, quality level: {quality}')

print(f'Sum of quality levels: {sum}')