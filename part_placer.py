import math


#TODO: link up with part database to get dimension information for bounding box generation
#Placeholder dimensions for part classes
part_dimensions = {"fuselage":{"x_width":5, "y_height":5, "z_depth":5},
					"parallel_wing": {"x_width":20, "y_height":2, "z_depth":5},
					"vertical_propeller": {"x_width":2, "y_height":2.5, "z_depth":2},
					"horizontal_propeller": {"x_width":2, "y_height":2, "z_depth":2.5}
					}
					# "non_parallel_wing": {"x_width":14.85, "y_height":14.85, "z_depth":5}}
					'''bounding box formula for non-parallel wings:
						x_width = cos(theta)*length + sin(theta)*thickness
						y_height = sin(theta)*length + cos(theta)*thickness 
					'''

class bounding_box
	def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):
		self.min_x = min_x
		self.max_x = max_x
		self.min_y = min_y
		self.max_y = max_y
		self.min_z = min_z
		self.max_z = max_z

class part
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


class design
	def __init__(self, parts = [], bounding_boxes = []):
		self.bounding_boxes = bounding_boxes
		self.parts = parts

	#TODO: inefficient boolean, should be able to reduce to three or
	def check_interference(box1, box2):
		if (box1.min_x < box2.max_x) or (box1.max_x > box2.min_x) or (box2.min_x < box1.max_x) or (box2.max_x > box1.min_x):
			if (box1.min_y < box2.max_y) or (box1.max_y > box2.min_y) or (box2.min_y < box1.max_y) or (box2.max_y > box1.min_y):
				if (box1.min_z < box2.max_z) or (box1.max_z > box2.min_z) or (box2.min_z < box1.max_z) or (box2.max_z > box1.min_z):
					return True
		return False


	def add_bounding_box(new_box):
		for bounding_box1 in self.bounding_boxes:
			for bounding_box2 in self.bounding_boxes:
				if check_interference(bounding_box1,bounding_box2):
					return False
		self.bounding_boxes.append(new_box)
		return True

	def add_part(part):
		if add_bounding_box(part.bounding_box):
			self.parts.append(part)
		else:
			print("Collision detected, failed to add part")




if __name__ == '__main__':
	input_file = open("generated_string.txt", 'r')

	input_string = input_file.readline()
	print(input_string)

	clusters = input_string.split("]")

	for i in range(len(clusters)):
		if len(clusters[i]) > 1:
			clusters[i] = clusters[i] + "]"
			print(clusters[i])
		else:
			clusters.remove(clusters[i])

	#TODO: implement marching cubes-like algorithm for part placement.
	for cluster in clusters:
		cursor = (0,0,0)






		



