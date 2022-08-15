import sys
import pickle

input_string_path = "topology_input.txt"
out_file_path = "topology_description.pkl"

out_file = open(out_file_path, 'wb')
target_string_file = open(input_string_path, 'r')

target_strings = target_string_file.readlines()


part_type_dict = {'f':0, 'w':0, 'p':0, 'h':0}

output_dict = {}

for target_string in target_strings:

	for token in target_string:
		if token in part_type_dict.keys():
			part_type_dict[token] += 1


	while part_type_dict['w'] > part_type_dict['f']*2:
			part_type_dict['f'] += 1

	class Fuselage:

		def __init__(self, uid, naca_1 = None, naca_2 = None, front = None, back = None):
			self.naca_1 = naca_1
			self.naca_2 = naca_2
			self.front = front
			self.back = back
			self.uid = uid
			self.type = "Fuselage"


		def get_connections(self):
			return [('naca_1', self.naca_1), ('naca_2',self.naca_2), ('front', self.front), ('back', self.back)]


	class Wing:

		def __init__(self, uid, naca = None):
			self.naca = naca
			self.uid = uid
			self.type = "Wing"

		def get_connections(self):
			return [('naca', self.naca)]


	class Propeller_unit:

		def __init__(self, uid, baseplate_connector = None):
			self.baseplate_connector = baseplate_connector
			self.uid = uid
			self.type = 'Propeller_unit'

		def get_connections(self):
			return [('baseplate_connector', self.baseplate_connector)]


	class threeWayConnector:
		def __init__(self, uid, front_connector = None, bottom_connector = None, top_connector = None, open_ports = 3):
			self.top_connector = top_connector
			self.bottom_connector = bottom_connector
			self.front_connector = front_connector
			self.uid = uid
			self.type = "threeWayConnector"
			self.open_ports = open_ports

		def get_connections(self):
			return [('top_connector', self.top_connector), ('bottom_connector',self.bottom_connector),
			 ('front_connector', self.front_connector)]

	class fourWayConnector:
		def __init__(self, uid, front_connector = None, back_connector = None, bottom_connector = None, top_connector = None, open_ports = 4):
			self.top_connector = top_connector
			self.bottom_connector = bottom_connector
			self.front_connector = front_connector
			self.back_connector = back_connector
			self.uid = uid
			self.type = "fourWayConnector"
			self.open_ports = open_ports
		def get_connections(self):
			return [('top_connector', self.top_connector), ('bottom_connector',self.bottom_connector), 
			('front_connector', self.front_connector), ('back_connector', self.back_connector)]

	class design:

		def __init__(self, parts = []):
			self.parts = parts


	end_design = design()

	if part_type_dict ['f'] > 2:
		print("Too many fuselages")
		part_type_dict['f'] = 2
		part_type_dict['w'] = 4

	fuselage_counter = 0
	wing_counter = 0
	prop_counter = 0
	three_way_counter = 0
	four_way_counter = 0


	while part_type_dict ['f'] >= 1 and part_type_dict['w'] >= 2:
		current_fuselage = Fuselage(uid = "fuselage-{}".format(fuselage_counter))
		fuselage_counter += 1
		left_wing = Wing(uid = "wing-{}".format(wing_counter), naca = current_fuselage.uid)
		wing_counter += 1
		right_wing = Wing(uid = "wing-{}".format(wing_counter), naca = current_fuselage.uid)
		current_fuselage.naca_1 = left_wing.uid
		current_fuselage.naca_2 = right_wing.uid
		for part in end_design.parts:
			if part.type == "Fuselage":
				current_fuselage.back = part.uid
				part.front = current_fuselage.uid

		end_design.parts.append(current_fuselage)
		end_design.parts.append(left_wing)
		end_design.parts.append(right_wing)

		part_type_dict['f'] -= 1
		part_type_dict['w'] -= 2

	for part in end_design.parts:
		if part.type == "Fuselage":
			if part.back == None:
				new_connector = fourWayConnector(uid = "fourWay-{}".format(four_way_counter), front_connector = part.uid, open_ports = 3)
				part.back = new_connector.uid
				four_way_counter += 1
				end_design.parts.append(new_connector)
			if part.front == None:
				new_connector = fourWayConnector(uid = "fourWay-{}".format(four_way_counter), back_connector = part.uid, open_ports = 3)
				part.front = new_connector.uid
				four_way_counter += 1
				end_design.parts.append(new_connector)

	while part_type_dict['p'] >= 1:

			for part in end_design.parts:	
				if part.type == "fourWayConnector":
					if part.open_ports > 1:
						new_unit = Propeller_unit(uid = "prop_-{}".format(prop_counter))
						prop_counter += 1
						if part.top_connector == None:
							new_unit.baseplate_connector = part.uid
							part.top_connector = new_unit.uid
							part.open_ports -= 1
						elif part.bottom_connector == None:
							new_unit.baseplate_connector = part.uid
							part.bottom_connector = new_unit.uid
							part.open_ports -= 1
						else:
							print("Port error")
						end_design.parts.append(new_unit)
						part_type_dict['p'] -= 1
						break

					elif part.open_ports == 1:
						new_unit = Propeller_unit(uid = "prop_-{}".format(prop_counter))
						prop_counter += 1
						if part.back_connector == None:
							new_connector = fourWayConnector(uid="fourWay-{}".format(four_way_counter), front_connector = part.uid, top_connector = new_unit.uid, open_ports=2)
							part.back_connector = new_connector.uid
						elif part.front_connector == None:
							new_connector = fourWayConnector(uid="fourWay-{}".format(four_way_counter), back_connector = part.uid, top_connector = new_unit.uid, open_ports=2)
							part.front_connector = new_connector.uid
						four_way_counter += 1
						new_unit.baseplate_connector = new_connector.uid
						
						end_design.parts.append(new_connector)
						end_design.parts.append(new_unit)
						part_type_dict['p'] -= 1
						part.open_ports -= 1
						break
			

	while part_type_dict['h'] >= 1:

			for part in end_design.parts:
				if part.type == "fourWayConnector":
					if part.open_ports > 1:
						new_unit = Propeller_unit(uid = "prop_-{}".format(prop_counter))
						prop_counter += 1
						if part.top_connector == None:
							new_unit.baseplate_connector = part.uid
							part.top_connector = new_unit.uid
							part.open_ports -= 1
						else:
							new_unit.baseplate_connector = part.uid
							part.bottom_connector = new_unit.uid
							part.open_ports -= 1
						end_design.parts.append(new_unit)
						part_type_dict['h'] -= 1
						break

					elif part.open_ports == 1:
						new_unit = Propeller_unit(uid = "prop_-{}".format(prop_counter))
						prop_counter += 1
						if part.back_connector == None:
							new_connector = fourWayConnector(uid="fourWay-{}".format(four_way_counter), front_connector = part.uid, top_connector = new_unit.uid, open_ports=2)
							part.back_connector = new_connector.uid
						elif part.front_connector == None:
							new_connector = fourWayConnector(uid="fourWay-{}".format(four_way_counter), back_connector = part.uid, top_connector = new_unit.uid, open_ports=2)
							part.front_connector = new_connector.uid
						four_way_counter += 1
						part.front = new_connector.uid
						new_unit.baseplate_connector = new_connector.uid
						end_design.parts.append(new_connector)
						end_design.parts.append(new_unit)
						part_type_dict['h'] -= 1
						part.open_ports -= 1
						break


	string_dict = {}
	for part in end_design.parts:
		part_list = []
		for connection in part.get_connections():
			part_list.append(connection)
		string_dict[part.uid] = part_list

	output_dict[target_string.strip("\n")] = string_dict


# print(output_dict)

pickle.dump(output_dict, out_file)
out_file.close()


