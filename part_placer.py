import math
import copy
import sys
import random

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

def custom_encoder(design):
	output_string = '[\n  {\n  "connections": [\n  '
	for key in design.parts.keys():
		connections = design.parts[key].connections
		pid = design.parts[key].pid

		for conn_key in connections.keys():
			dest = connections[conn_key]
			if dest:
				dest_connections = design.parts[dest].connections
				for dest_key in dest_connections.keys():
					if dest_connections[dest_key] == pid:
						if not output_string[-1] == ' ':
							output_string += ",\n"
						if pid[0] in ['p', 'h']:
							motor = 'm' + pid[1:]
							motor_port = 'Base_Connector' 
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}},'.format(motor_port, dest_key, motor, dest)
							motor_port = 'Prop_Connector' 
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}},'.format('MOTOR_CONNECTOR_CS_IN', motor_port, pid, motor)
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}}'.format(motor_port, 'MOTOR_CONNECTOR_CS_IN',motor , pid)
						elif dest[0] in ['p', 'h']:
							motor = 'm' + pid[1:]
							motor_port = 'Base_Connector' 
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}},'.format(conn_key, motor_port, pid, motor)
							motor_port = 'Prop_Connector' 
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}},'.format('MOTOR_CONNECTOR_CS_IN', motor_port, pid, motor)
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}}'.format(motor_port, 'MOTOR_CONNECTOR_CS_IN',motor , pid)

						else:
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}}'.format(conn_key, dest_key, pid, dest)
	
	output_string += "],\n"
	output_string += '"design": "Generated",\n'
	output_string += '"instances": [\n '
	for key in design.parts.keys():
		print("encoder: part type: " + design.parts[key].part_type)
		print('---' + output_string[-1] + '---')
		print(output_string[-1] == '}'	)
		# if not output_string[-1] == ' ':
		if output_string[-1] == '}':	
			output_string += ',\n'
		if design.parts[key].part_type in ['p','h']:
			output_string += '{{\n'\
			'"assignment": {{}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}},'.format('MAGiDRIVE150','m' + design.parts[key].pid[1:])
		if design.parts[key].part_type == 'w':
			model_name = "naca_wing"
			output_string += '{{\n'\
			'"assignment": {{\n'\
			'"CHORD_1": "TopWingChord",\n'\
			'"CHORD_2": "TopWingChord",\n'\
			'"LOAD": "TopWingLoad",\n'\
			'"NACA_Profile": "TopWingNaca",\n'\
			'"SPAN": "TopWingSpan",\n'\
			'"THICKNESS": "TopWingThickness"\n'\
			'}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format(model_name,design.parts[key].pid)
		elif design.parts[key].part_type == 'p':
			model_name = "62x5_2_3200_46_1150"
			output_string += '{{\n'\
			'"assignment": {{\n'\
			'"Direction": "UpFacingCCW_Spin",\n'\
			'"Prop_type": "UpFacingCCW_PropType"\n'\
			'}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format(model_name,design.parts[key].pid)	
		elif design.parts[key].part_type == 'h':
			model_name = "62x5_2_3200_46_1150"
			output_string += '{{\n'\
			'"assignment": {{\n'\
			'"Direction": "FwdFacingCCW_Spin",\n'\
			'"Prop_type": "FwdFacingCCW_PropType"\n'\
			'}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format(model_name,design.parts[key].pid)
		elif design.parts[key].part_type == 'c':
			model_name = "PORTED_CYL"
			output_string += '{{\n'\
			'"assignment": {{\n'\
			'"DIAMETER": "CylinderDiameter",\n'\
			'"LENGTH": "CylinderLength"\n'\
			'}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format(model_name,design.parts[key].pid)
		elif design.parts[key].part_type == 'f':
			model_name = "FUSE_SPHERE_CYL_CONE"
			output_string += '{{\n'\
			'"assignment": {{\n'\
			'"FLOOR_HEIGHT": "FuselageFloorHeight",\n'\
			'"LENGTH": "FuselageLength",\n'\
			'"MIDDLE_LENGTH": "FuselageMiddleLength",\n'\
			'"PORT_THICKNESS": "FuselagePortThickness",\n'\
			'"SEAT_1_FB": "FuselageSeatFB",\n'\
			'"SEAT_1_LR": "FuselageSeat1LR",\n'\
			'"SEAT_2_FB": "FuselageSeatFB",\n'\
			'"SEAT_2_LR": "FuselageSeat2LR",\n'\
			'"SPHERE_DIAMETER": "FuselageSphereDiameter",\n'\
			'"TAIL_DIAMETER": "FuselageTailDiameter"\n'\
			'}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format(model_name,design.parts[key].pid)

		else:
			output_string += '{{\n'\
			'"assignment": {{}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format('',design.parts[key].pid)	

	output_string += "],"
	output_string += '"parameters":{\n'\
		'"BatteryLeftMountSide": "2",\n'\
		'"BatteryPercent": "100",\n'\
		'"BatteryRightMountSide": "1",\n'\
		'"BatteryVoltage": "840",\n'\
		'"BottomWingChord": "4000",\n'\
		'"BottomWingLoad": "2000",\n'\
		'"BottomWingNaca": "0012",\n'\
		'"BottomWingSpan": "1000",\n'\
		'"BottomWingThickness": "12",\n'\
		'"CylinderDiameter": "200",\n'\
		'"CylinderLength": "1650",\n'\
		'"FuselageFloorHeight": "150",\n'\
		'"FuselageLength": "2000",\n'\
		'"FuselageMiddleLength": "300",\n'\
		'"FuselagePortThickness": "150",\n'\
		'"FuselageSeat1LR": "210",\n'\
		'"FuselageSeat2LR": "-210",\n'\
		'"FuselageSeatFB": "790",\n'\
		'"FuselageSphereDiameter": "1520",\n'\
		'"FuselageTailDiameter": "200",\n'\
		'"FwdFacingCCW_PropType": "-1",\n'\
		'"FwdFacingCCW_Spin": "-1",\n'\
		'"FwdFacingCW_PropType": "1",\n'\
		'"FwdFacingCW_Spin": "1",\n'\
		'"Requested_Lateral_Speed_1": "25",\n'\
		'"TailCylinderPortThickness": "150",\n'\
		'"TailWingChord": "1000",\n'\
		'"TailWingLeftAngle": "45",\n'\
		'"TailWingLoad": "1000",\n'\
		'"TailWingNaca": "0012",\n'\
		'"TailWingRightAngle": "315",\n'\
		'"TailWingSpan": "4500",\n'\
		'"TailWingThickness": "12",\n'\
		'"TopWingChord": "1000",\n'\
		'"TopWingLoad": "10000",\n'\
		'"TopWingNaca": "2418",\n'\
		'"TopWingSpan": "10000",\n'\
		'"TopWingThickness": "18",\n'\
		'"UpFacingCCW_PropType": "-1",\n'\
		'"UpFacingCCW_Spin": "-1",\n'\
		'"UpFacingCW_PropType": "1",\n'\
		'"UpFacingCW_Spin": "1"\n'\
		'}}]'			

	return output_string
	

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
class part():
	def __init__(self, pid, part_type = 'p', centroid = (0,0,0), x_width = 1, y_height = 1, z_depth = 1):
		self.centroid = centroid
		self.x_width = x_width
		self.y_height = y_height
		self.z_depth = z_depth
		self.part_type = part_type
		self.pid = pid
		self.connections = {}
		min_x = centroid[0] - x_width/2
		max_x = centroid[0] + x_width/2
		min_y = centroid[1] - y_height/2
		max_y = centroid[1] + y_height/2
		min_z = centroid[2] - z_depth/2
		max_z = centroid[2] + z_depth/2
		self.bounding_box = bounding_box(min_x, max_x, min_y, max_y, min_z, max_z)
		# print('part: ' + str(self.pid))
		# print(self.centroid)
		# self.bounding_box.print_bounds()


	#TODO: add a complex bounding box for non_parallel wings. Worst case scenario: set of consecutive, contiguous, cuboid bounding boxes.
	#Theta should be in radians
	def calculate_non_parallel_wing_bounding_box(theta, x_width, y_height, z_depth):
		functional_x_width = math.cos(theta)*x_width + math.sin(theta)*y_height
		functional_y_height = math.sin(theta)*x_width + math.cos(theta)*y_height
		return (functional_x_width,functional_y_height,z_depth)

	def add_connection(self, src, dst):
		self.connections[src] = dst

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.pid, 
			sort_keys=True, indent=4)

class connector(part):
	def __init__(self, pid, centroid = [0,0,0], buffer_connector = False):
		part.__init__(self, pid, part_type = 'c')
		self.centroid = centroid
		self.buffer_connector = buffer_connector
		self.connections = {'front': None, 'rear' : None, 'top': None, 'bottom': None, 'left': None, 'right': None}

	def toJSON(self):
		return '{"pid":' + json.dumps(self, default=lambda o: o.pid, 
			sort_keys=True, indent=4) + '}'

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
	def __init__(self, parts = {}, bounding_boxes = [], clusters = []):
		self.bounding_boxes = bounding_boxes
		self.parts = parts
		self.connector_id_count = 0
		self.part_id_count = 0
		self.initial_connector = connector("c" + str(self.connector_id_count))
		self.add_part(self.initial_connector)
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
		if not part.part_type == 'c':
			if self.add_bounding_box(part.bounding_box):
				self.parts[part.pid] = part
			else:
				print("Collision detected, failed to add part")
		else:
			self.parts[part.pid] = part

	def print_parts_and_centroids(self):
		for key in self.parts.keys():
			part = self.parts[key]
			# if not part.part_type == 'c':
			# 	print(part.pid)
			# 	part.bounding_box.print_bounds()
			print(part.pid)	
			part.bounding_box.print_bounds()

	def z_bound_check(self, part, z_min, z_max):
		if part.bounding_box.max_z > z_max:
			z_max = part.bounding_box.max_z
		if part.bounding_box.min_z > z_min:
			z_min = part.bounding_box.min_z
		return z_min, z_max

	def get_buffer_connectors(self, z = None):
		buffer_connectors = []
		for key in self.parts.keys():
			part = self.parts[key]
			if part.part_type == 'bc':
				if z:
					if part.centroid[2] == z:
						buffer_connectors.append(part)
				else:
					buffer_connectors.append(part)

		return buffer_connectors 

	def find_valid_buffer(self, z_bound, minimum_position, direction):
		possible_connectors = self.get_buffer_connectors(z = z_bound)
		# minimum_position = x_bound + ((subcluster_width/2) * direction)
		for connector in possible_connectors:
			if direction == 1:
				if connector.centroid[0] >= minimum_position:
					return connector
			else:
				if connector.centroid[0] <= minimum_position:
					return connector
		return None

	def determine_quadrant(self, schema, index, centered):
		centered_adder = 1 if centered else 0
		print(schema)
		if schema == "Staggered":
			return (index + centered_adder) % 4
		if schema == "Inverse Staggered":
			return ((index + centered_adder) % 4) + 2
		if schema == "Grouped":
			return ((index + centered_adder) % 2)
		if schema == "Inverse Grouped":
			return ((index + centered_adder) % 2) + 2

			

	#set clusters in order they should be processed (center, fuselage containing cluster first, left, then right.)
	def order_clusters(self):
		new_clusters = []
		for cluster in self.clusters:
			if 'f' in cluster:
				new_clusters = [cluster] + new_clusters
			else:
				new_clusters.append(cluster)

		self.clusters = new_clusters



	#Main function call for placing parts in 3d space
	#TODO: possible replace cursor list with a class for readability
	def place_all_parts(self):

		# Create cursors to track position both in front of and behind base
		cursor = [0,0,0]
		front_cursor = [0,0,0]
		rear_cursor = [0,0,0]
		z_min = 0
		z_max = 0

		# Create an alternator for going between front and rear when placing clusters
		alternator = 1

		direction = "front"
		cluster = self.clusters[0]
		# print("cursor being handed")
		# print(cursor)
		connector = self.frontmost_connector
		cursor, z_min, z_max = self.place_cluster_pos_lock(cluster, cursor, connector, direction)
		temporary_z_buffer = 10
		rear_cursor[2] += z_min
		rear_cursor[2] -= temporary_z_buffer
		front_cursor[2] += z_max
		front_cursor[2] += temporary_z_buffer


		#For each cluster, identify a connector to branch off of and a cursor to use. Update cursors from maxes of last iteration and place
		temporary_z_buffer = 10
		for cluster  in self.clusters[1:]:
			if alternator == -1:
				connector = self.frontmost_connector
				rear_cursor[2] += z_min
				rear_cursor[2] -= temporary_z_buffer
				cursor = front_cursor
				direction = "front"
			else:
				front_cursor[2] += z_max
				front_cursor[2] += temporary_z_buffer
				connector = self.rearmost_connector
				cursor = rear_cursor
				direction = "rear"
			# print("cursor being handed")
			# print(cursor)
			cursor, z_min, z_max = self.place_cluster_pos_lock(cluster, cursor, connector, direction)

			alternator *= -1

	#Place clusters where parts' centroids have the same z value

	#Account for number of separate connector clusters
	def place_cluster_pos_lock(self, cluster, cursor, origin_connector, direction = "front"):

		#Count subclusters and track where they start/end
		subcluster_count = 0
		tokens = cluster
		subcluster_boundaries = []
		subclusters = []
		i = 0
		while i < len(tokens):
			
			if tokens[i] == '(':
				subcluster_count += 1
				subcluster_start = i
				subcluster_end = tokens.index(')',i)
				subclusters.append(tokens[subcluster_start+1:subcluster_end])
				cutting_floor = subcluster_start if subcluster_start == 0 else subcluster_start
				cutting_roof = subcluster_end + 1 if subcluster_end == len(tokens)-1 else subcluster_end + 1

				tokens = tokens[:subcluster_start] + tokens[subcluster_end+1:]
				schema = 'even' if (subcluster_count % 2 == 0) else 'odd'
			else:

				i += 1

		i = 0
		subcluster_index = 0
		subcluster_processing_order = []
		subcluster_boundary_index = len(subclusters)//2
		subcluster_boundary_offset = 0
		subcluster_boundary_alternator = 1
		j = 0 
		# print(subclusters)
		while j < len(subclusters):
			subcluster_processing_order.append(subclusters[
				subcluster_boundary_index + (subcluster_boundary_offset * 
					subcluster_boundary_alternator)])
			subcluster_boundary_alternator *= -1
			# print(subcluster_boundary_index + (subcluster_boundary_offset * 
			# 		subcluster_boundary_alternator))
			if j % 2 == 0:
				subcluster_boundary_offset += 1
			j += 1

		# print(subcluster_processing_order)
		# print(tokens)

		new_tokens = []
		
		k = 0 
		
		alternator = -1
		offset = 0

		#-x direction
		leftmost = [x for x in cursor]

		#+x direction
		rightmost = [x for x in cursor]

		# Count tokens in current cluster
		w_count = 0
		l_count = 0
		p_count = 0
		h_count = 0
		for token in tokens:
				w_count += 1 if token == 'w' else 0
				l_count += 1 if token == 'l' else 0
				p_count += 1 if token == 'p' else 0
				h_count += 1 if token == 'h' else 0

		#track how far we've moved along principle axis, forward or rearward
		z_max = 0
		z_min = 0

		#fuselage cluster
		if 'f' in tokens and not self.initial_fuselage_placed:
			string_index = tokens.index('f')

			# Get dimensions of fuselage, create is for fuselage, add part to design
			fuselage_dimensions = part_dimensions['f']
			fuselage_id = 'f' + str(self.part_id_count)
			self.part_id_count += 1
			new_part = part(fuselage_id ,centroid=cursor, part_type='f', x_width=fuselage_dimensions["x_width"], y_height=fuselage_dimensions["y_height"], z_depth=fuselage_dimensions["z_depth"])
			self.add_part(new_part)

			# Track min and max z for incrementation (this will be repeated without comment)
			z_min, z_max = self.z_bound_check(new_part, z_min, z_max)

			# connect single initial connector to front fuselage, and connect rear of connector to front of fuselage
			self.frontmost_connector.connections["rear"] = fuselage_id
			self.parts[fuselage_id].connections['front'] = self.frontmost_connector.pid

			# create rear connector, connect front of rear connector to rear of fuselage
			new_connector = connector('c' + str(self.connector_id_count))
			new_connector.connections["front"] = fuselage_id
			self.parts[fuselage_id].connections['rear'] = new_connector.pid
			self.connector_id_count += 1
			self.rearmost_connector = new_connector
			self.add_part(new_connector)

			# If there are two wings
			if w_count == 2:

				# Create temporary cursor for placing parts. Start on left wing, moving cursor by fuselage/2
				temp_cursor = [cursor[0] - fuselage_dimensions["x_width"]/2, cursor[1], cursor[2]]

				# Grab dimensions of the wing and move cursor to new wing centroic
				dimensions = part_dimensions['w']
				temp_cursor[0] -= dimensions["x_width"]/2

				# Create new part id and create new wing, place at current temp cursor location
				new_id = 'w' + str(self.part_id_count)
				self.part_id_count += 1
				new_part = part(new_id, centroid = [temp_cursor[0],temp_cursor[1],temp_cursor[2]], part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])

				# Connect wing to fuselage and add part
				new_part.connections["naca"] = fuselage_id
				self.parts[fuselage_id].connections['naca1'] = new_part.pid
				self.add_part(new_part)
				z_min, z_max = self.z_bound_check(new_part, z_min, z_max)

				# Move cursor to other side of fuselage + half of wing width to reach centroid
				temp_cursor = [temp_cursor[0] + dimensions['x_width'], temp_cursor[1], temp_cursor[2]]
				temp_cursor[0] += dimensions['x_width']
				temp_cursor[0] += fuselage_dimensions['x_width']

				# Create new part id and create new wing, place at current temp cursor location
				new_id = 'w' + str(self.part_id_count)
				new_part = part(new_id, centroid = [temp_cursor[0],temp_cursor[1],temp_cursor[2]], part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				self.part_id_count += 1

				# Connect wing to fuselage and add part
				new_part.connections["naca"] = fuselage_id
				self.parts[fuselage_id].connections['naca2'] = new_part.pid
				self.add_part(new_part)
				z_min, z_max = self.z_bound_check(new_part, z_min, z_max)

				# Add propeller on top of fuselage, if specified
				if 'p' in tokens:
					# Create temporary cursor for placing parts. Start on top of fuselage
					temp_cursor[1] += fuselage_dimensions["y_height"]/2

					# Grab dimensions for vertical propeller, move cursor to centroid
					dimensions = part_dimensions['p']
					temp_cursor[1] += direction["y_height"]/2

					# Create new part and add to design, set connections
					new_id = 'p' + str(self.part_id_count)
					self.part_id_count += 1
					new_part = part(new_id, centroid = temp_cursor, part_type = 'p', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					new_part.connections["baseplate"] = fuselage_id
					self.parts[fuselage_id].connections['top'] = new_part.pid
					self.add_part(new_part)
					z_min, z_max = self.z_bound_check(new_part, z_min, z_max)

			# If there are 4 wings and a fuselage
			if w_count == 4:
				# Create temporary cursor for placing parts. Start on top of fuselage
				temp_cursor = [cursor[0], cursor[1]+ fuselage_dimensions["y_height"]/2, cursor[2]]

				#Create a connector flush with the top of the fuselage, connect it to top of fuselage
				new_connector = connector('c' + str(self.connector_id_count))
				new_connector.connections['bottom'] = fuselage_id
				self.parts[fuselage_id].connections['top'] = new_connector.pid
				self.add_part(new_connector)
				self.connector_id_count += 1

				# Create new wing, move temporary cursor higher to prevent collisions, as well as to the left for first wing centroid
				new_id = 'w' + str(self.part_id_count)
				self.part_id_count += 1
				dimensions = part_dimensions['w']
				temp_cursor = [temp_cursor[0] - dimensions['x_width']/2, temp_cursor[1]+ dimensions["y_height"]/2, temp_cursor[2]]
				new_wing = part(part(new_id, centroid = temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"]))
				new_wing.connections['naca'] = new_connector.pid
				self.parts[new_connector.pid].connections['left'] = new_id
				self.add_part(new_wing)

				# Move temp cursor to second wing centroid position, add new wing
				new_id = 'w' + str(self.part_id_count)
				self.part_id_count += 1
				dimensions = part_dimensions['w']
				temp_cursor[0] += dimensions['x_width']
				new_wing = part(part(new_id, centroid = temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"]))
				new_wing.connections['naca'] = new_connector.pid
				self.parts[new_connector.pid].connections['right'] = new_id
				self.add_part(new_wing)

				# Add connector to bottom of fuselage
				new_connector = connector('c' + str(self.connector_id_count))
				new_connector.connections['top'] = fuselage_id
				self.parts[fuselage_id].connections['bottom'] = new_connector.pid
				self.add_part(new_connector)
				self.connector_id_count += 1

				# Move temp cursor below fuselage
				temp_cursor[1] -= fuselage_dimensions["y_height"]
				temp_cursor[1] -= dimensions["y_height"]

				# add third wing (bottom right)
				new_id = 'w' + str(self.part_id_count)
				self.part_id_count += 1
				new_wing = part(part(new_id, centroid = temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"]))
				new_wing.connections['naca'] = new_connector.pid
				self.parts[new_connector.pid].connections['right'] = new_id
				self.add_part(new_wing)

				# move temp cursor to left side
				temp_cursor[0] -= dimensions["x_width"]

				# add last wing
				new_id = 'w' + str(self.part_id_count)
				self.part_id_count += 1
				new_wing = part(part(new_id, centroid = temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"]))
				new_wing.connections['naca'] = new_connector.pid
				self.parts[new_connector.pid].connections['left'] = new_id
				self.add_part(new_wing)



				# Add first wing

		elif w_count >= 2:
			


			pass
		elif 'l' in tokens:
			pass
		else:

			temp_cursor = [x for x in cursor]
			string_index = len(tokens)//2
			centered = len(tokens) % 2 == 1

			# Add perpendicular connector to start attatching parts
			# TODO: fix issue with utilizing f + non w
			base_connector = connector('c' + str(self.connector_id_count))
			self.connector_id_count += 1
			origin_connector.connections[direction] = base_connector.pid
			if direction == 'front':
				base_connector.connections["right"] = origin_connector.pid
			else:
				base_connector.connections["left"] = origin_connector.pid
			self.add_part(base_connector)
			leftmost_connector = base_connector
			rightmost_connector = base_connector

			# print("i is" + str(i))
			i = 0

			while i < len(tokens):

				dimensions = part_dimensions[tokens[string_index + (offset * alternator)]]
				#The first part gets centered on the cursor, the following are placed either to the left or right
				if i == 0 and centered:

					# Add the first, centered part
					new_part = part(tokens[i] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count +=1
					self.add_part(new_part)

					# Update the left and right most positions
					rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
					leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]

					#Update the cursor position
					temp_cursor = leftmost

					#Connect the base to the base connector (different for horizontal and vertical)
					new_part.connections["baseplate"] = base_connector.pid
					if new_part.part_type == 'h':
						base_connector.connections['right'] = new_part.pid
					else:
						base_connector.connections['top'] = new_part.pid

					# Increment the offset
					offset += 1

				else:

					# Move the cursor to the new centroid and add the current part there
					temp_cursor = [temp_cursor[0] + (dimensions["x_width"]/2 * alternator), temp_cursor[1], temp_cursor[2]]
					new_part = part(tokens[i] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count +=1

					# Add a buffer connector
					buffer_connector = connector('bc' + str(self.connector_id_count),centroid = temp_cursor, buffer_connector = True)

					if alternator == -1:

						# Attach buffer connecter, create and attach new connector to hold part
						buffer_connector.connections['rear'] = leftmost_connector.pid
						leftmost_connector.connections['front'] = buffer_connector.pid
						self.connector_id_count += 1
						new_connector = connector('c' + str(self.connector_id_count))
						self.connector_id_count += 1
						buffer_connector.connections['front'] = new_connector.pid
						new_connector.connections['rear'] = buffer_connector.pid
						self.add_part(new_connector)

						# Update leftmost position and connector
						leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
						leftmost_connector = new_connector
						temp_cursor = [x for x in rightmost]
					else:

						# Attach buffer connecter, create and attach new connector to hold part
						buffer_connector.connections['front'] = rightmost_connector.pid
						rightmost_connector.connections['rear'] = buffer_connector.pid
						self.connector_id_count += 1
						new_connector = connector('c' + str(self.connector_id_count))
						self.connector_id_count += 1
						buffer_connector.connections['rear'] = new_connector.pid
						new_connector.connections['front'] = buffer_connector.pid
						

						# Update rightmost position and connector
						rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
						rightmost_connector = new_connector
						temp_cursor = [x for x in leftmost]
						offset += 1
					# Attach part and new connector
					new_part.connections['baseplate'] = new_connector.pid
					if new_part.part_type == 'h':
						new_connector.connections[direction] = new_part.pid
					else:
						new_connector.connections['top'] = new_part.pid
					# self.print_parts_and_centroids()
					self.add_part(buffer_connector)
					self.add_part(new_connector)
					self.add_part(new_part)
					alternator *= -1
				if dimensions["z_depth"] > z_max:
					z_max = dimensions["z_depth"]
				i += 1
			


		# Set/select schema for part and subcluster placement
		schema_types = ["Staggered", "Inverse Staggered", "Grouped", "Inverse Grouped"]
		part_schema = schema_types[random.randint(0,len(schema_types)-1)]
		subcluster_schema = 'centered' if subcluster_count == 1 else schema_types[random.randint(0,len(schema_types)-1)]


		

		# Reset cursor to middle
		temp_cursor = [x for x in cursor]

		#Set boundaries for placing
		top_leftmost_bound = temp_cursor[0]
		bottom_leftmost_bound = temp_cursor[0]
		top_rightmost_bound = temp_cursor[0]
		bottom_rightmost_bound = temp_cursor[0]
		bounds = [top_leftmost_bound, top_rightmost_bound, bottom_leftmost_bound, bottom_rightmost_bound]

		 

		# Process subclusters
		for i in range(len(subcluster_processing_order)):
		# for subcluster in subcluster_processing_order:

			# If we have an odd subcluster # and we're at the first subcluster, we'll be placing using the middle connector
			if i == 0 and len(subcluster_processing_order) % 2 == 1:
				centered = True
			else:
				#if not, find out the max possible x_size of the cluster
				x_sum = 0
				for token in subcluster_processing_order[i]:
					x_width = part_dimensions[token]["x_width"]
					x_sum += x_width

				# detemine which quadrant the branching connector will be placed in
				quadrant = self.determine_quadrant(part_schema, i, len(subcluster_processing_order)%2 == 1)

				# Determine the direction of cursor movement, as well as the minimum distance of the buffer connector
				direction = -1 if quadrant in [0,2] else 1
				x_bound = bounds[quadrant]
				minimum_position = x_bound + ((x_width/2) * direction)

				# Try to find a valid buffer connector
				buffer_connector = self.find_valid_buffer(cursor[2], minimum_position, direction)

				# If a valid buffer connector does not exist, add a new one and connect it to the appropriate edge connector
				if not buffer_connector:
					new_buffer = connector('bc' + str(self.connector_id_count), buffer_connector = True)
					self.connector_id_count += 1

					if direction == 1:
						new_centroid = [x for x in rightmost_connector.centroid]
						new_centroid[0] = minimum_position + 1
						new_buffer.centroid = new_centroid
						self.parts[rightmost_connector.pid].connections['rear'] = new_buffer.pid
						rightmost_connector = new_buffer

					else:
						new_centroid = [x for x in leftmost_connector.centroid]
						new_centroid[0] = minimum_position - 1
						new_buffer.centroid = new_centroid
						self.parts[leftmost_connector.pid].connections['front'] = new_buffer.pid
						leftmost_connector = new_buffer
					buffer_connector = new_buffer

					self.add_part(buffer_connector)

				# Place the subcluster using the buffer as a connection point, get new left/right bounds
				sub_z_min, sub_z_max, bound = self.place_cluster_separate_connector(subcluster_processing_order[i], 
					temp_cursor, part_schema = schema, subcluster_schema = subcluster_schema, subcluster_index = i, quadrant = quadrant,
					 origin_connector = buffer_connector)
				subcluster_index += 1

				# Update the bound of the corresponding quadrant
				if quadrant in [0,2]:
					bounds[quadrant] = min([bound, bounds[quadrant]])
				else:
					bounds[quadrant] = max([bound, bounds[quadrant]])

				# Update z_max for incrementing
				# TODO: Consider chainging to z_bound_check function later	
				z_max = sub_z_max if sub_z_max > z_max else z_max
				z_min = sub_z_min if sub_z_min > z_min else z_min
			
		return temp_cursor, z_max, z_min


	#Place clusters that are on a separate connector from the principal connector
	def place_cluster_separate_connector(self, tokens, cursor, origin_connector, subcluster_schema = 'Grouped', subcluster_index = 0, part_schema = "Grouped", deviation = 10, z_max = 0, quadrant = 0):

		alternator = -1
		offset = 0
		directions = [-1,1,-1,1]
		y_directions = [1,1,-1,-1]
		vertical_connection = ["top", "top", "bottom", "bottom"]
		rising_connection = ["front", "front", "rear", "rear"]
		rising_connector = connector('c' + str(self.connector_id_count))
		self.connector_id_count += 1
		rising_connector.connections["rear"] = origin_connector.pid
		self.parts[origin_connector.pid].connections[vertical_connection[quadrant]] = rising_connector.pid

		temp_cursor = [x for x in cursor]
		string_index = len(tokens)//2
		centered = len(tokens) % 2 == 1

		# Add perpendicular connector to start attatching parts
		# TODO: fix issue with utilizing f + non w
		base_connector = connector('c' + str(self.connector_id_count))
		self.connector_id_count += 1
		rising_connector.connections[rising_connection[quadrant]] = base_connector.pid
		# if direction == 'front':
		# 	base_connector.connections["right"] = origin_connector.pid
		# else:
		# 	base_connector.connections["left"] = origin_connector.pid

		base_connector.connections[vertical_connection[(quadrant + 2) % 4]] = rising_connector.pid
		self.add_part(rising_connector)
		self.add_part(base_connector)
		leftmost_connector = base_connector
		rightmost_connector = base_connector
		leftmost = [x for x in cursor]
		rightmost = [x for x in cursor]


		i = 0

		while i < len(tokens):

			dimensions = part_dimensions[tokens[string_index + (offset * alternator)]]
			#The first part gets centered on the cursor, the following are placed either to the left or right
			if i == 0 and centered:

				# Add the first, centered part
				new_part = part(tokens[i] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				self.part_id_count +=1
				self.add_part(new_part)

				# Update the left and right most positions
				rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
				leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]

				#Update the cursor position
				temp_cursor = leftmost

				#Connect the base to the base connector (different for horizontal and vertical)
				new_part.connections["baseplate"] = base_connector.pid
				if new_part.part_type == 'h':
					base_connector.connections['right'] = new_part.pid
				else:
					base_connector.connections['top'] = new_part.pid

				# Increment the offset
				offset += 1

			else:

				# Move the cursor to the new centroid and add the current part there
				temp_cursor = [temp_cursor[0] + (dimensions["x_width"]/2 * alternator), temp_cursor[1], temp_cursor[2]]
				new_part = part(tokens[i] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[i], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				self.part_id_count +=1

				# Add a buffer connector
				buffer_connector = connector('bc' + str(self.connector_id_count),centroid = temp_cursor, buffer_connector = True)

				if alternator == -1:

					# Attach buffer connecter, create and attach new connector to hold part
					buffer_connector.connections['rear'] = leftmost_connector.pid
					self.connector_id_count += 1
					new_connector = connector('c' + str(self.connector_id_count))
					self.connector_id_count += 1
					buffer_connector.connections['front'] = new_connector.pid
					new_connector.connections['rear'] = buffer_connector.pid
					self.add_part(new_connector)

					# Update leftmost position and connector
					leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
					leftmost_connector = new_connector
					temp_cursor = [x for x in rightmost]
				else:

					# Attach buffer connecter, create and attach new connector to hold part
					buffer_connector.connections['front'] = rightmost_connector.pid
					self.connector_id_count += 1
					new_connector = connector('c' + str(self.connector_id_count))
					self.connector_id_count += 1
					buffer_connector.connections['rear'] = new_connector.pid
					new_connector.connections['front'] = buffer_connector.pid
					

					# Update rightmost position and connector
					rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
					rightmost_connector = new_connector
					temp_cursor = [x for x in leftmost]
					offset += 1
				# Attach part and new connector
				new_part.connections['baseplate'] = new_connector.pid
				if new_part.part_type == 'h':
					new_connector.connections['right'] = new_part.pid
				else:
					new_connector.connections['top'] = new_part.pid
				# self.print_parts_and_centroids()
				self.add_part(buffer_connector)
				self.add_part(new_connector)
				self.add_part(new_part)
				alternator *= -1
			if dimensions["z_depth"] > z_max:
				z_max = dimensions["z_depth"]
			i += 1

		return_values = [leftmost,rightmost,leftmost,rightmost]

		return return_values[quadrant]


	def print_parts(self):
		for key in self.parts.keys():
			# print(self.parts[key])
			print(self.parts[key].pid)
			print(self.parts[key].connections)
			print(self.parts[key].toJSON())


if __name__ == '__main__':

	new_clusters = []

	# [['h','p','h'],['w','f','w'],['h','p','h']]
	# [['h','p','h'],['w','f','w'],['p'],['(','h','h',')']]
	#['(', 'p', 'p', ')','(', 'p', 'p', ')','(', 'p', 'p', ')']

	#['w','f','w'],
	#['p','p','p']
	#[['(', 'p', 'p', 'p', ')','(', 'p', 'p', ')','p','(', 'p', 'p', 'p', ')','p','(', 'p', 'p', ')','(', 'p', 'p', 'p', ')',],
	#['(', 'p', 'p', ')','p','p','p','(', 'p', 'p', ')']]
	#['(', 'p', 'p', ')', 'h', '(', 'p', 'p',')' ]
	#['h','p','h'],['w','f','w'],['h','p','h']
	clusters = [['(', 'p', 'p', ')', 'h', 'h', '(', 'p', 'p',')' ],['w','f','w'],['(', 'p', 'p', ')', 'h', 'h','(', 'p', 'p',')' ]]
	new_design = design(clusters = clusters)
	new_design.place_all_parts()
	output = custom_encoder(new_design)
	output_file = open("generated_design.txt", 'w')
	output_file.write(output)

	response = input("Print output?")

	if response == 'y':
		print(output)	
