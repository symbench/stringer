import math


#TODO: link up with part database to get dimension information for bounding box generation
#Placeholder dimensions for part classes
token_to_part_dict
part_dimensions = {"f":{"x_width":5, "y_height":5, "z_depth":5},
					"w'": {"x_width":20, "y_height":2, "z_depth":5},
					"p": {"x_width":2, "y_height":2.5, "z_depth":2},
					"h": {"x_width":2, "y_height":2, "z_depth":2.5}}
					# "non_parallel_wing": {"x_width":14.85, "y_height":14.85, "z_depth":5}}
					# """bounding box formula for non-parallel wings:
					# 	x_width = cos(theta)*length + sin(theta)*thickness
					# 	y_height = sin(theta)*length + cos(theta)*thickness 
					# """

#Define a bounding box class for use in checking for collisions
class bounding_box:
	def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):
		self.min_x = min_x
		self.max_x = max_x
		self.min_y = min_y
		self.max_y = max_y
		self.min_z = min_z
		self.max_z = max_z

#Define a part class for containing bounding box and/or any future information that will be critical to the part (ports, orientation requirements, etc.)
class part:
	def __init__(self, centroid = (0,0,0), x_width = 1, y_height = 1, z_depth = 1):
		self.centroid = centroid
		self.x_width = x_width
		self.y_height = y_height
		self.z_depth = z_depth
		min_x = centroid[0] - x_width/2
		max_x = centroid[0] + x_width/2
		min_y = centroid[0] - y_height/2
		max_y = centroid[0] + y_height/2
		min_z = centroid[0] - z_depth/2
		max_z = centroid[0] + z_depth/2
		self.bounding_box = bounding_box(min_x, max_x, min_y, max_y, min_z, max_z)

	#TODO: add a complex bounding box for non_parallel wings. Worst case scenario: set of consecutive, contiguous, cuboid bounding boxes.
	#Theta should be in radians
	def calculate_non_parallel_wing_bounding_box(theta, x_width, y_height, z_depth):
		functional_x_width = math.cos(theta)*x_width + math.sin(theta)*y_height
		functional_y_height = math.sin(theta)*x_width + math.cos(theta)*y_height
		return (functional_x_width,functional_y_height,z_depth)

#Cluster class for string segments. May not be necessary
#TODO: change this class to consider individual parts and separate connector groups as tokens
class cluster:
	def __init__(self, tokens = [], positionally_locked = False, separate_connector = False):
		self.tokens = tokens
		self.positionally_locked = positionally_locked
		self.separate_connector = separate_connector

#Design class for holding and calculating everything relevant to the design's part placement including
#bounding boxes, parts, clusters and the functions for parsing and placing those items
class design:
	def __init__(self, parts = [], bounding_boxes = [], clusters = []):
		self.bounding_boxes = bounding_boxes
		self.parts = parts
		self.order_clusters(clusters)

	#TODO: inefficient boolean, should be able to reduce to three or
	def check_interference(self, box1, box2):
		if (box1.min_x < box2.max_x) or (box1.max_x > box2.min_x) or (box2.min_x < box1.max_x) or (box2.max_x > box1.min_x):
			if (box1.min_y < box2.max_y) or (box1.max_y > box2.min_y) or (box2.min_y < box1.max_y) or (box2.max_y > box1.min_y):
				if (box1.min_z < box2.max_z) or (box1.max_z > box2.min_z) or (box2.min_z < box1.max_z) or (box2.max_z > box1.min_z):
					return True
		return False

	#Simoltaneously check for conflicts and add new bounding box
	def add_bounding_box(self, new_box):
		for bounding_box1 in self.bounding_boxes:
			for bounding_box2 in self.bounding_boxes:
				if check_interference(bounding_box1,bounding_box2):
					return False
		self.bounding_boxes.append(new_box)
		return True
	#Add a part, calls bounding box check
	def add_part(self, part):
		if add_bounding_box(part.bounding_box):
			self.parts.append(part)
		else:
			print("Collision detected, failed to add part")

	#set clusters in order they should be processed (center, fuselage containing cluster first, left, then right.)
	def order_clusters(self, clusters):
		new_clusters = []
		for cluster in clusters:
			if 'f' in cluster:
				new_clusters = [cluster] + new_clusters
			else:
				new_clusters.append(cluster)

		print(new_clusters)
		self.clusters = new_clusters


	# def add_clusters_from_string(self, string):
	# 	 i = 0
	# 	 while i < len(string):
	# 	 	if string[i] == "[":
	# 	 		j = string.find("]")
	# 	 		if "(" in string[i+1:j]:
		 			
	# 	 			new_cluster = cluster(tokens = [x for x in string[i+1:j]],)


	#Main function call for placing parts in 3d space
	#TODO: possible replace cursor list with a class for readability
	def place_all_parts(self):
		for cluster  in self.clusters:
			cursor = [0,0,0]
			if cluster[0] = '[':
				cursor = place_cluster_pos_lock(cluster, cursor)
			elif cluster[0] = '(':
				cursor = place_cluster_separate_connector(cluster, cursor, schema = 'centered', deviation = 'above')
			else:
				cursor = place_individual_part(cluster, cursor)

	#Place clusters where parts' centroids have the same z value

	#TODO: implement following flowchart
	#Account for number of separate connector clusters
	#
	def place_cluster_pos_lock(cluster, cursor):
		subcluster_count = 0
		tokens = cluster.tokens
		for token in tokens:
			if token = '(':
				subcluster_count += 1
		subcluster_placement_style = 'even' if (subcluster_count % 2 == 0) else 'odd'
		subcluster_index = 0
		i = 0
		while i < len(tokens):
			if tokens[i] = "(":
				schema = subcluster_placement_check(style, subcluster_index)
				deviation = 'above' if ((subcluster_index//2) % 2 == 0) else 'below'
				subcluster_end_index = tokens[i:].index(")")
				place_cluster_separate_connector(tokens[i:subcluster_end_index], cursor, schema = schema, deviation = deviation)


			i += 1

	#Place clusters that are on a separate connector from the principal connector
	def place_cluster_separate_connector(tokens, cursor, schema = 'centered', deviation = 'above', offset = 10,  endcap = 'false'):
		#To return to principal connector we record original cursor position
		original_cursor = [cursor[0], cursor[1] + offset, cursor[2]]
		z_max = 0
		i = 0
		string_index = len(tokens)//2
		#-x direction
		leftmost = cursor[0]
		#+x direction
		rightmost = cursor[0]
		while i < len(tokens):
			alternator = -1
			dimensions = part_dimensions(tokens[string_index])
			try:
				#The first part gets centered on the cursor, the following are placed either to the left or rig ht
				if i == 0:
					self.add_part(part(centroid=cursor, x_width=dimensions[0], y_height=dimensions[1], z_depth=dimensions[2]))
					rightmost = [cursor[0] + dimensions[0]/2, cursor[1], cursor[2]]
					leftmost = [cursor[0] - dimensions[0]/2, cursor[1], cursor[2]]
					cursor = [cursor[0] + (dimensions[0]/2 * alternator), cursor[1], cursor[2]]
				else:
					cursor = [cursor[0] + (dimensions[0]/2 * alternator), cursor[1], cursor[2]]
					self.add_part(part(centroid=cursor, x_width=dimensions[0], y_height=dimensions[1], z_depth=dimensions[2]))
					if alternator == -1:
						leftmost = [cursor[0] - dimensions[0]/2, cursor[1], cursor[2]]
						cursor = [x for x in rightmost]
					else:
						rightmost = [cursor[0] + dimensions[0]/2, cursor[1], cursor[2]]
						cursor = [x for x in leftmost]
					alternator *= -1
			except:
				print("Part created collision! Part type:{}, part centroid:{}, bounding box dimensions: ({},{},{}). Exiting.".format)
			if dimensions[2] > z_max:
				z_max = dimensions[2]



	def subcluster_placement_check(style, index):
		if style == 'even':
			return 'left' if index% 2 == 0 else 'right'
		elif style == 'odd':
			if index == 0:
				return 'centered'
			elif index% 2 == 0:
				return 'right'
			else:
				return 'left'







if __name__ == '__main__':
	input_file = open("../../Downloads/generated_string.txt", 'r')

	input_string = input_file.readline()
	print(input_string)

	#TODO: Change clusters to be groups of brackets, groups inside parentheses, as well as terminal tokens outside of brackets
	clusters = input_string.split("]")

	for i in range(len(clusters)):
		if len(clusters[i]) > 1:
			clusters[i] = clusters[i] + "]"
			# print(clusters[i])
		else:
			clusters.remove(clusters[i])

	new_clusters = []

	#TODO: implement marching cubes-like algorithm for part placement.
	cursor = [0,0,0]
	for cluster in clusters:
		processed_tokens = []
		j = 1
		for i in range(len(cluster)):
			if cluster[i] == "'":
				processed_tokens[i-j] = processed_tokens[i-j] + cluster[i]
				j += 1
			else:
				processed_tokens.append(cluster[i])
		for entry in processed_tokens:
			print(entry)
		print("END CLUSTER")
		new_clusters.append(cluster(tokens = processed_tokens, positionally_locked = (processed_tokens[0] == '['), 
			separate_connector = (processed_tokens[0] == '(') ))

	design = design(clusters=new_clusters)




