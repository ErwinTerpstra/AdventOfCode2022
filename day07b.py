def sumDirectorySize(directory):
	totalSize = 0

	for file in directory['files']:
		totalSize += file['size']

	for name, subdirectory in directory['directories'].items():
		totalSize += sumDirectorySize(subdirectory)

	directory['totalSize'] = totalSize

	return totalSize

def flattenDirectory(directory, result):
	result.append(directory)

	for name, subdirectory in directory['directories'].items():
		result = flattenDirectory(subdirectory, result)

	return result

with open("day07_input.txt") as file:
	lines = [ line.rstrip('\n') for line in file ]
	
	rootDirectory = { 'files': [ ], 'directories': { } }
	directoryStack = [ rootDirectory ]

	for line in lines:
		if line == '':
			continue

		currentDirectory = directoryStack[-1]
		chunks = line.split(' ')

		if line.startswith('$'):
			# Commands
			if chunks[1] == 'cd':
				subdir = chunks[2]

				# Check if we want to navigate down or up
				if subdir != '..':
					if not subdir in currentDirectory['directories']:
						currentDirectory['directories'][subdir] = { 'files': [ ], 'directories': { } }

					directoryStack.append(currentDirectory['directories'][subdir])
				else:
					directoryStack.pop()

			elif chunks[1] == 'ls':
				# We don't actually need to do anything here, any "not-command" line is assumed to be part of ls
				pass
			else:
				raise Exception(f'Invalid command {chunks[1]}')
		else:
			# File listing
			if chunks[0] != 'dir':
				currentDirectory['files'].append({ 'name': chunks[1], 'size': int(chunks[0]) })

	sumDirectorySize(rootDirectory)
	
	allDirectories = flattenDirectory(rootDirectory, [ ])
	allDirectories.sort(key=lambda x: x['totalSize'])

	freeSpace = 70000000 - rootDirectory['totalSize']
	requiredSpace = 30000000 - freeSpace

	for directory in allDirectories:
		if directory['totalSize'] >= requiredSpace:
			print(directory['totalSize'])
			break
	