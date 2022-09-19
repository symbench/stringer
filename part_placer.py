import math



#TODO: link up with part database to get dimension information for bounding box generation
#Placeholder dimensions for part classes
part_dimensions = {"f":{"x_width":5, "y_height":5, "z_depth":5},
					"w": {"x_width":20, "y_height":2, "z_depth":5},
					"p": {"x_width":2, "y_height":2.5, "z_depth":2},
					"h": {"x_width":2, "y_height":2, "z_depth":2.5}}
					# "non_parallel_wing": {"x_width":14.85, "y_height":14.85, "z_depth":5}}
					# """bounding box formula for non-parallel wings:
					# 	x_width = cos(theta)*length + sin(theta)*thickness
					# 	y_height = sin(theta)*length + cos(theta)*thickness 
					# """


class connector:
	def __init__(self, pid):
		self.pid = pid
		self.connections = {'front': None, 'back' : None, 'top': None, 'bottom': None, 'left': None, 'right': None}

#Define a bounding box class for use in checking for collisions
class bounding_box:
	def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):
		self.min_x = min_x
		self.max_x = max_x
		self.min_y = min_y
		self.max_y = max_y
		self.min_z = min_z
		self.max_z = max_z
	def print_bounds(self):
		print("x [{},{}], y [{},{}], z [{},{}]".format(str(self.min_x), str(self.max_x),str(self.min_y), str(self.max_y),str(self.min_z), str(self.max_z)))

#Define a part class for containing bounding box and/or any future information that will be critical to the part (ports, orientation requirements, etc.)
class part:
	def __init__(self, pid, part_type = 'p', centroid = (0,0,0), x_width = 1, y_height = 1, z_depth = 1):
		self.centroid = centroid
		self.x_width = x_width
		self.y_height = y_height
		self.z_depth = z_depth
		self.part_type = part_type
		self.connections = {}
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

	def add_connection(self, src, dst):
		self.connections[src] = dst

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
		self.connector_id_count = 0
		self.part_id_count = 0
		self.initial_connector = connector("connector_" + str(self.connector_id_count))
		self.connector_id_count += 1
		self.connectors = {}
		self.frontmost_connector = self.initial_connector
		self.rearmost_connector = self.initial_connector
		self.initial_fuselage_placed = False
		self.clusters = clusters
		self.order_clusters()

	#TODO: inefficient boolean, should be able to reduce to three or
	def check_interference(self, box1, box2):
		if (box1.max_x > box2.min_x and box1.max_x < box2.max_x) or (box1.min_x > box2.min_x and box1.min_x < box2.max_x) or ((box1.min_x < box2.min_x and box1.max_x > box2.max_x)):
			if (box1.max_y > box2.min_y and box1.max_y < box2.max_y) or (box1.min_y > box2.min_y and box1.min_y < box2.max_y) or ((box1.min_y < box2.min_y and box1.max_y > box2.max_y)):
				if (box1.max_z > box2.min_z and box1.max_z < box2.max_z) or (box1.min_z > box2.min_z and box1.min_z < box2.max_z) or ((box1.min_z < box2.min_z and box1.max_z > box2.max_z)):
					return True
		return False

	#Simoltaneously check for conflicts and add new bounding box
	def add_bounding_box(self, new_box):
		for bounding_box1 in self.bounding_boxes:
			for bounding_box2 in self.bounding_boxes:
				if self.check_interference(bounding_box1,bounding_box2):
					return False
		self.bounding_boxes.append(new_box)
		return True
	#Add a part, calls bounding box check
	def add_part(self, part):
		if self.add_bounding_box(part.bounding_box):
			self.parts.append(part)
		else:
			print("Collision detected, failed to add part")

	#set clusters in order they should be processed (center, fuselage containing cluster first, left, then right.)
	def order_clusters(self):
		new_clusters = []
		for cluster in self.clusters:
			if 'f' in cluster:
				new_clusters = [cluster] + new_clusters
			else:
				new_clusters.append(cluster)

		# print(new_clusters)
		self.clusters = new_clusters



	#Main function call for placing parts in 3d space
	#TODO: possible replace cursor list with a class for readability
	def place_all_parts(self):
		cursor = [0,0,0]
		alternator = -1
		for cluster  in self.clusters:
			if alternator == -1:
				connector = self.frontmost_connector
			else:
				connector = self.rearmost_connector
			cursor = self.place_cluster_pos_lock(cluster, cursor, connector)

	#Place clusters where parts' centroids have the same z value

	#TODO: implement following flowchart
	#Account for number of separate connector clusters
	def place_cluster_pos_lock(self, cluster, cursor, origin_connector, direction = "front"):
		subcluster_count = 0
		tokens = cluster
		subcluster_boundaries = []
		i = 0
		for i in range(len(tokens)):
			if tokens[i] == '(':
				subcluster_count += 1
				subcluster_start = i
				subcluster_end = tokens.index(')',i)
				subcluster_boundaries.append([subcluster_start,subcluster_end])
				schema = 'even' if (subcluster_count % 2 == 0) else 'odd'
		subcluster_index = 0

		while subcluster_index < subcluster_count:
			subcluster_indices = subcluster_boundaries[subcluster_index]
			start = subcluster_indices[0]
			end = subcluster_indices[1]
			self.place_cluster_separate_connector(tokens[start+1:end], cursor, schema = schema, subcluster_index = subcluster_index)
			subcluster_index += 1
		alternator = -1
		offset = 0
		#-x direction
		leftmost = [x for x in cursor]
		#+x direction
		rightmost = [x for x in cursor]
		z_max = 0
		if 'f' in tokens and not self.initial_fuselage_placed:
			string_index = tokens.index('f')
			dimensions = part_dimensions['f']
			fuselage_id = 'f' + str(self.part_id_count)
			self.part_id_count += 1
			new_part = part(fuselage_id ,centroid=cursor, part_type='f', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
			self.add_part(new_part)
			self.frontmost_connector.connections["back"] = fuselage_id
			new_connector = connector(self.connector_id_count)
			self.connector_id_count += 1
			new_connector.connections["front"] = fuselage_id
			self.rearmost_connector = new_connector
			w_count = 0
			l_count = 0
			p_count = 0
			for token in tokens:
				w_count += 1 if token == 'w' else 0
				l_count += 1 if token == 'l' else 0
				p_count += 1 if token == 'p' else 0
			if w_count == 2:
				temp_cursor = temp_cursor = [cursor[0] - dimensions["x_width"]/2, cursor[1], cursor[2]]
				dimensions = part_dimensions['w']
				temp_cursor[0] -= dimensions["x_width"]/2
				new_id = 'w' + str(self.part_id_count)
				self.part_id_count += 1
				new_part = part(new_id, centroid = temp_cursor, part_type = 'p', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				new_part.connections["baseplate"] = fuselage_id
				self.add_part(new_part)
			if 'p' in tokens:
				temp_cursor = [cursor[0], cursor[1]+ dimensions["y_height"]/2, cursor[2]]
				dimensions = part_dimensions['p']
				temp_cursor[1] += direction["y_height"]/2
				new_id = 'p' + str(self.part_id_count)
				self.part_id_count += 1
				new_part = part(new_id, centroid = temp_cursor, part_type = 'p', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				new_part.connections["baseplate"] = fuselage_id
				self.add_part(new_part)
		elif 'w' in tokens:
			pass
		elif 'l' in tokens:
			pass
		else:
			string_index = len(tokens)//2
			centered = len(tokens) % 2 == 1
			while i < len(tokens):
				dimensions = part_dimensions[tokens[string_index + (offset * alternator)]]
				#The first part gets centered on the cursor, the following are placed either to the left or right
				if i == 0 and centered:
					new_part = part(tokens[i] + str(self.part_id_count), centroid=cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count +=1
					self.add_part(new_part)
					rightmost = [cursor[0] + dimensions["x_width"]/2, cursor[1], cursor[2]]
					leftmost = [cursor[0] - dimensions["x_width"]/2, cursor[1], cursor[2]]
					cursor = [cursor[0] + (dimensions["x_width"] / 2 * alternator), cursor[1], cursor[2]]
					offset += 1
				else:
					cursor = [cursor[0] + (dimensions["x_width"]/2 * alternator), cursor[1], cursor[2]]
					self.add_part(part(tokens[i] + str(self.part_id_count), centroid=cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"]))
					self.part_id_count +=1
					# print("added a part")
					if alternator == -1:
						leftmost = [cursor[0] - dimensions["x_width"]/2, cursor[1], cursor[2]]
						cursor = [x for x in rightmost]
					else:
						rightmost = [cursor[0] + dimensions["x_width"]/2, cursor[1], cursor[2]]
						cursor = [x for x in leftmost]
						offset += 1
					alternator *= -1
				if dimensions["z_depth"] > z_max:
					z_max = dimensions["z_depth"]
				i += 1
		return cursor







	#Place clusters that are on a separate connector from the principal connector
	def place_cluster_separate_connector(self, tokens, cursor, schema = 'even', subcluster_index = 0, deviation = 10, z_max = 0):
		
		#To return to principal connector we record original cursor position
		# print(cursor[1], deviation)
		deviation *= -1 if subcluster_index == 1 else 1
		original_cursor = [cursor[0], cursor[1] + deviation, cursor[2]]
		i = 0
		offset = 0
		string_index = len(tokens)//2
		centered = len(tokens) % 2 == 1
		#-x direction
		leftmost = [x for x in cursor]
		#+x direction
		rightmost = [x for x in cursor]
		alternator = -1
		while i < len(tokens):
			dimensions = part_dimensions[tokens[string_index + (offset * alternator)]]
			# try:
			#The first part gets centered on the cursor, the following are placed either to the left or rig ht
			if i == 0 and centered:
				new_part = part(tokens[i] + str(self.part_id_count),centroid=cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				self.part_id_count +=1
				self.add_part(new_part)
				# print("added a part")
				rightmost = [cursor[0] + dimensions["x_width"]/2, cursor[1], cursor[2]]
				leftmost = [cursor[0] - dimensions["x_width"]/2, cursor[1], cursor[2]]
				cursor = [cursor[0] + (dimensions["x_width"] / 2 * alternator), cursor[1], cursor[2]]
				offset += 1
				print(cursor)
				# print(dimensions["x_width"])
				# new_part.bounding_box.print_bounds()
			else:
				cursor = [cursor[0] + (dimensions["x_width"]/2 * alternator), cursor[1], cursor[2]]
				self.add_part(part(tokens[i] + str(self.part_id_count), centroid=cursor, x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"]))
				self.part_id_count +=1
				# print("added a part")
				if alternator == -1:
					leftmost = [cursor[0] - dimensions["x_width"]/2, cursor[1], cursor[2]]
					cursor = [x for x in rightmost]
				else:
					rightmost = [cursor[0] + dimensions["x_width"]/2, cursor[1], cursor[2]]
					cursor = [x for x in leftmost]
					offset += 1
				alternator *= -1
			if dimensions["z_depth"] > z_max:
				z_max = dimensions["z_depth"]
			i += 1
		return cursor, z_max


if __name__ == '__main__':

	new_clusters = []


	clusters = [['h','p','h'],['w','f','w'],['p'],['(','h','h',')']]
	new_design = design(clusters = clusters)
	new_design.place_all_parts()
	# new_cursor = new_design.place_cluster_separate_connector('phphp',[0,0,0])
	



