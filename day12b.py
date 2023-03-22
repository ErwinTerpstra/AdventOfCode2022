heights = \
{
	'S': 0,
	'E': 26
}

class GridNode:
	def __init__(self, x, y, height):
		self.x = x
		self.y = y
		self.height = height
		self.distance = -1
		self.parent = None

class Grid:

	def __init__(self, grid):
		self.height = len(grid)
		self.width = len(grid[0])

		self.target_node = None
		
		self.nodes = [ ]

		# Create node objects for each cell
		for (y, row) in enumerate(grid):
			for (x, cell) in enumerate(row):
				
				node = GridNode(x, y, heights.get(cell, ord(cell) - ord('a')))

				if cell == 'E':
					self.target_node = node
				
				self.nodes.append(node)


	def get_node(self, x, y):
		return self.nodes[y * self.width + x]

	def neighbours(self, node):
		if node.x > 0:
			yield self.get_node(node.x - 1, node.y)
		if node.y > 0:
			yield self.get_node(node.x, node.y - 1)
		if node.x < self.width - 1:
			yield self.get_node(node.x + 1, node.y)
		if node.y < self.height - 1:
			yield self.get_node(node.x, node.y + 1)
	
	def reset(self):
		for node in self.nodes:
			node.distance = -1
			node.parent = None

	def find_path(self, start_node, target_node):
		self.reset()
		
		# Set distance on start node
		start_node.distance = 0

		open_list = [ start_node ]
		path_found = False

		while len(open_list) > 0:
			node = open_list.pop(0)

			if node == target_node:
				path_found = True
				continue

			for neighbour in grid.neighbours(node):
				if neighbour.height > node.height + 1:
					continue

				if neighbour.distance == -1 or neighbour.distance > node.distance + 1:
					neighbour.distance = node.distance + 1
					neighbour.parent = node

					open_list.append(neighbour)

		path = [ ]

		if not path_found:
			return None
		
		current = target_node

		while current != start_node:
			path.insert(0, current)
			current = current.parent

		return path

with open("day12_input.txt") as file:
	grid = [ list(line.rstrip('\n')) for line in file ]

grid = Grid(grid)
shortest_path = -1

for node in grid.nodes:
	if node.height > 0:
		continue

	path = grid.find_path(node, grid.target_node)

	if path == None:
		continue

	if shortest_path == -1 or len(path) < shortest_path:
		shortest_path = len(path)
		
print(shortest_path)