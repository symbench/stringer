import math
import copy
import sys
import random
import argparse

#TODO: link up with part database to get dimension information for bounding box generation
#Placeholder dimensions for part classes
part_dimensions = {"f":{"x_width":5, "y_height":5, "z_depth":5},
					"w": {"x_width":20, "y_height":2, "z_depth":5},
					"p": {"x_width":2, "y_height":2.5, "z_depth":2},
					"h": {"x_width":2, "y_height":2, "z_depth":2.5},
					"cg": {"x_width":5, "y_height":5, "z_depth":5},
					"l" : {"x_width":1, "y_height":6, "z_depth":2}}
					# "non_parallel_wing": {"x_width":14.85, "y_height":14.85, "z_depth":5}}
					# """bounding box formula for non-parallel wings:
					# 	x_width = cos(theta)*length + sin(theta)*thickness
					# 	y_height = sin(theta)*length + cos(theta)*thickness 
					# """

def parse_clusters(text):
	clusters = []

	return clusters



def custom_encoder(design, design_num, remove_boilerplate = True):
	output_string = '[\n  {\n  "connections": [\n  '
	parameters = [
	# ("Front_Rail_Length", "80"),
	# ("Front_Wing_Tube_Length", "55"),
	# ("FwdFacingCCW_PropType", "-1"),
	# ("FwdFacingCCW_Spin", "1"),
	# ("FwdFacingCW_Spin", "1"),
	# ("Mid_Tube_Length", "140"),
	# ("NACA_profile", "0012"),
	# ("Param_11", "180"),
	# ("Param_12", "90"),
	# ("Param_14", "448.68"),
	# ("Rear_Rail_Length", "220"),
	# ("Rudder_Tube_Length", "41"),
	# ("Top_Leg_Tube_Length", "150.1524"),
	# ("Vertical_Tube_Length", "150"),
	# ("angle_270", "270"),
	# ("front_l_wing_offset", "289.68"),
	# ("front_r_wing_offset", "160.32"),
	# ("front_wing_chord", "150"),
	# ("front_wing_span", "450"),
	("fuse_floor", "20", False),
	("Orient_Z_ANGLE", "90", False),
	("fuse_height", "105",False),
	("fuse_width", "80",False),
	("l_rudder_offset", "90",False),
	("r_rudder_offset", "50",False),
	("rear_wing_chord", "180",False),
	("rear_wing_offset", "90",False),
	("rear_wing_span", "609",False),
	("rudder_chord", "100",False),
	("rudder_span", "140",False),
	("wing_thickness", "12",False)]

	type_parameters = {
	'p' : [("Direction", "Direction", False, "-1"), ("Prop_type", "Prop_type", False, "1")],
	'h' : [("Direction", "Direction", False, "-1"), ("Prop_type", "Prop_type", False, "1")],
	'w' : [("AILERON_BIAS","AILERON_BIAS", False, "0.5" ),  ("CHORD_1", "wing_chord", True, "150"),("CHORD_2", "wing_chord", True, "150"), ("CONTROL_CHANNEL", "CONTROL_CHANNEL", False, "1"),
	("FLAP_BIAS", "FLAP_BIAS", False, "0.5"),("LOAD", "LOAD", False, "30"), ("NACA_Profile", "NACA_Profile", False, "0012"),("SERVO_LENGTH", "SERVO_LENGTH", False, "0.1"),
	("SERVO_THICKNESS", "SERVO_THICKNESS", False, "0.1"),("SERVO_WIDTH", "SERVO_WIDTH", False, "0.1"), ("SPAN", "SPAN", False, "1200"), ("TAPER_OFFSET", "TAPER_OFFSET", False, "0"),
	("THICKNESS", "THICKNESS", False, "12"),("TUBE_DIAMETER", "TUBE_DIAMETER", False, "7.1474"),("TUBE_OFFSET", "TUBE_OFFSET", False, "600"), ("TUBE_ROTATION", "TUBE_ROTATION", False, "180")],
	'l': [("AILERON_BIAS","AILERON_BIAS", False, "0.5" ),  ("CHORD_1", "wing_chord", True, "150"),("CHORD_2", "wing_chord", True, "150"), ("CONTROL_CHANNEL", "CONTROL_CHANNEL", False, "1"),
	("FLAP_BIAS", "FLAP_BIAS", False, "0.5"),("LOAD", "LOAD", False, "30"), ("NACA_Profile", "NACA_Profile", False, "0012"),("SERVO_LENGTH", "SERVO_LENGTH", False, "0.1"),
	("SERVO_THICKNESS", "SERVO_THICKNESS", False, "0.1"),("SERVO_WIDTH", "SERVO_WIDTH", False, "0.1"), ("SPAN", "SPAN", False, "1200"), ("TAPER_OFFSET", "TAPER_OFFSET", False, "0"),
	("THICKNESS", "THICKNESS", False, "12"),("TUBE_DIAMETER", "TUBE_DIAMETER", False, "7.1474"),("TUBE_OFFSET", "TUBE_OFFSET", False, "600"), ("TUBE_ROTATION", "TUBE_ROTATION", False, "180")],
	't' : [("BASE_ROT", "BASE_ROT", False, "0"),("END_ROT", "END_ROT", False, "0"),("Length", "Length", False, "100"),("Offset1", "Offset1", False, "0"),("Offset2Offset2", "Offset2", False, "0")],
	'pt' : [("BASE_ROT", "BASE_ROT", False, "0"),("END_ROT", "END_ROT", False, "0"),("Length", "Length", False, "100"),("Offset1", "Offset1", False, "0"),("Offset2Offset2", "Offset2", False, "0")],
	'bc' : [("ANGHORZCONN", "ANGHORZCONN", False, "90"),("ANGVERTCONN", "ANGVERTCONN", False, "0"),("DIAMETER", "DIAMETER", False, "7.1474")],
	'c' : [("ANGHORZCONN", "ANGHORZCONN", False, "90"),("ANGVERTCONN", "ANGVERTCONN", False, "0"),("DIAMETER", "DIAMETER", False, "7.1474")],
	'fl' : [("BOTTOM_ANGLE", "BOTTOM_ANGLE", False, "0"),("SIDE_ANGLE", "SIDE_ANGLE", False, "0")],
	'm' : [("CONTROL_CHANNEL", "CONTROL_CHANNEL", False)],
	'f' : [("BOTTOM_CONNECTOR_OFFSET_LENGTH","BOTTOM_CONNECTOR_OFFSET_LENGTH", False, "0" ),  ("BOTTOM_CONNECTOR_OFFSET_WIDTH", "BOTTOM_CONNECTOR_OFFSET_WIDTH", False, "0"),("BOTTOM_CONNECTOR_ROTATION", "BOTTOM_CONNECTOR_ROTATION", True, "0"), 
	("BOTTOM_CONNECTOR_ROTATION", "BOTTOM_CONNECTOR_ROTATION", False, "0"),
	("FLOOR_CONNECTOR_1_DISP_WIDTH", "FLOOR_CONNECTOR_1_DISP_WIDTH", False, "30"),("FLOOR_CONNECTOR_2_DISP_LENGTH", "FLOOR_CONNECTOR_2_DISP_LENGTH", False, "0"), ("FLOOR_CONNECTOR_2_DISP_WIDTH", "FLOOR_CONNECTOR_2_DISP_WIDTH", False, "-30"),("FLOOR_CONNECTOR_3_DISP_LENGTH", "FLOOR_CONNECTOR_3_DISP_LENGTH", False, "-160"),
	("FLOOR_CONNECTOR_3_DISP_WIDTH", "FLOOR_CONNECTOR_3_DISP_WIDTH", False, "13"),("FLOOR_CONNECTOR_4_DISP_LENGTH", "FLOOR_CONNECTOR_4_DISP_LENGTH", False, "-160"), ("FLOOR_CONNECTOR_4_DISP_WIDTH", "FLOOR_CONNECTOR_4_DISP_WIDTH", False, "-18"), ("FLOOR_CONNECTOR_5_DISP_LENGTH", "FLOOR_CONNECTOR_5_DISP_LENGTH", False, "115"),
	("FLOOR_CONNECTOR_5_DISP_WIDTH", "FLOOR_CONNECTOR_5_DISP_WIDTH", False, "0"),("FLOOR_CONNECTOR_6_DISP_LENGTH", "FLOOR_CONNECTOR_6_DISP_LENGTH", False, "155"),("FLOOR_CONNECTOR_6_DISP_WIDTH", "FLOOR_CONNECTOR_6_DISP_WIDTH", False, "18"), ("FLOOR_CONNECTOR_7_DISP_LENGTH", "FLOOR_CONNECTOR_7_DISP_LENGTH", False, "-120"),
	("FLOOR_CONNECTOR_7_DISP_WIDTH", "FLOOR_CONNECTOR_7_DISP_WIDTH", False, "0"),("FLOOR_CONNECTOR_8_DISP_LENGTH", "FLOOR_CONNECTOR_8_DISP_LENGTH", False, "155"),("FLOOR_CONNECTOR_8_DISP_WIDTH", "FLOOR_CONNECTOR_8_DISP_WIDTH", False, "-18"), ("FLOOR_HEIGHT", "FLOOR_HEIGHT", False, "20"),
	("FUSE_CYL_LENGTH", "FUSE_CYL_LENGTH", False, "270"),("HORZ_DIAMETER", "HORZ_DIAMETER", False, "190"),("VERT_DIAMETER", "VERT_DIAMETER", False, "125")],
	'cg' : [("Rotation", "Rotation", False, "0")]
	}

	default_value_dict = {}

	for key in type_parameters.keys():
		for param in type_parameters[key]:
			if len(param) >= 4:
				default_value_dict[param[1]] = param[3]


	uav_type_models = {
	'm' : 'kde_direct_KDE2315XF_885', 'fl' : '0394_para_flange', 't' : '0394OD_para_tube',
	'w' : 'Wing_horiz_hole', 'l': 'Wing_horiz_hole', 'p' : 'apc_propellers_7x5E','h' : 'apc_propellers_7x5E', 'c' : '0394od_para_hub_4',
	'f' : 'capsule_fuselage', 'cg' : 'CargoCase'
	}

	def generate_instance_params(pid, part_type):
		return_string = ''
		return_parameters = []
		for param in type_parameters[part_type]:
			value = param[1] if param[2] else pid + '_' + param[1]
			return_string += '"{}" : "{}",\n'.format(param[0], value)
			return_parameters.append((value, value, param[2]))
		return_string = return_string[:-2]
		return_string += "\n"

		return return_string, return_parameters


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
						if design.parts[key].part_type in ['p', 'h']:
							output_string = output_string[:-2]
						elif design.parts[dest].part_type in ['p', 'h']:
							if design.uav:
								motor = 'm' + dest[1:]
								motor_anchor_port = 'Base_Connector' 
								motor_propeller_port = 'Prop_Connector' 
								flange = 'fl' + dest[1:]
								flange_anchor_port = 'BottomConnector'
								flange_motor_port = "TopConnector"
								prop_tube = 'pt' + dest[1:]
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format(conn_key, flange_anchor_port, pid, flange) 
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format(flange_anchor_port, conn_key, flange, pid) 
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format(flange_motor_port, motor_anchor_port, flange, motor)
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format(motor_anchor_port, flange_motor_port, motor, flange)
								# output_string += '{{'\
								# '"connector1": "{}",\n'\
								# '"connector2": "{}",\n'\
								# '"instance1": "{}",\n'\
								# '"instance2": "{}"\n'\
								# '}},'.format("EndConnection", motor_anchor_port, prop_tube, motor)
								# output_string += '{{'\
								# '"connector1": "{}",\n'\
								# '"connector2": "{}",\n'\
								# '"instance1": "{}",\n'\
								# '"instance2": "{}"\n'\
								# '}},'.format(motor_anchor_port, "EndConnection", motor, prop_tube) 
								# output_string += '{{'\
								# '"connector1": "{}",\n'\
								# '"connector2": "{}",\n'\
								# '"instance1": "{}",\n'\
								# '"instance2": "{}"\n'\
								# '}},'.format('MOTOR_CONNECTOR_CS_IN', motor_propeller_port, pid, motor) 
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format(motor_propeller_port, 'MOTOR_CONNECTOR_CS_IN',motor , dest)
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format('MOTOR_CONNECTOR_CS_IN', motor_propeller_port,dest , motor)
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}},'.format("MotorPower", "MotorPower", "BatteryController", motor)
								output_string += '{{'\
								'"connector1": "{}",\n'\
								'"connector2": "{}",\n'\
								'"instance1": "{}",\n'\
								'"instance2": "{}"\n'\
								'}}'.format("MotorPower", "MotorPower", motor, "BatteryController")
							else:
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
								'}}'.format(motor_port, 'MOTOR_CONNECTOR_CS_IN',motor , pid)

						#TODO: change to dictionary system for cargo/fuselage/etc.
						else:
							connector_port = conn_key
							dest_port = dest_key
							uav_conversions = {'left': 'Side_Connector_1', 'front': 'Side_Connector_2', 'right': 'Side_Connector_3', 'rear': 'Side_Connector_4', 'top': 'Top_Connector', 'bottom': 'Bottom_Connector'}
							part_type = design.parts[pid].part_type
							if part_type == 'c':
								connector_port = uav_conversions[conn_key]
							elif part_type == 'cg':
								#disable
								connector_port = 'Case2HubConnectore' #RUIN NAME TO REMOVE CASE
							part_type = design.parts[dest].part_type
							if part_type == 'c':
								dest_port = uav_conversions[dest_key]
							elif part_type == 'cg':
								#disable
								dest_port = 'Case2HubConnectore' ##RUIN NAME TO REMOVE CASE

							source_name = 'fuselage' if pid[0] == 'f' else pid
							dest_name = 'fuselage' if dest[0] == 'f' else dest
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}}'.format(connector_port, dest_port, source_name, dest_name)
						if design.parts[dest].part_type == 'w':
							# output_string = output_string[:-1]
							output_string += ',\n'
							connector_port = 'Wing_Servo_Connector'
							dest_port = 'Connector'
							source_name = dest
							dest_name = 'servo' + dest[1:]
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}},'.format(connector_port, dest_port, source_name, dest_name)
							output_string += '{{'\
							'"connector1": "{}",\n'\
							'"connector2": "{}",\n'\
							'"instance1": "{}",\n'\
							'"instance2": "{}"\n'\
							'}}'.format(dest_port, connector_port, dest_name, source_name)

						

	boiler_plate_connections = [
	{'connector1': 'FloorConnector1', 'connector2': 'Bottom_Connector', 'instance1':'fuselage', 'instance2':'Main_Battery'},
	{'connector1': 'BatteryPower', 'connector2': 'PowerBus', 'instance1':'BatteryController', 'instance2':'Main_Battery'},
	{'connector1': 'SensorConnector', 'connector2': 'FloorConnector3', 'instance1':'RpmTemp', 'instance2':'fuselage'},
	{'connector1': 'SensorConnector', 'connector2': 'FloorConnector4', 'instance1':'Current', 'instance2':'fuselage'},
	{'connector1': 'SensorConnector', 'connector2': 'FloorConnector5', 'instance1':'Autopilot', 'instance2':'fuselage'},
	{'connector1': 'SensorConnector', 'connector2': 'FloorConnector6', 'instance1':'Voltage', 'instance2':'fuselage'},
	{'connector1': 'SensorConnector', 'connector2': 'FloorConnector7', 'instance1':'GPS', 'instance2':'fuselage'},
	{'connector1': 'SensorConnector', 'connector2': 'FloorConnector8', 'instance1':'Variometer', 'instance2':'fuselage'},
	{'connector1': 'CargoConnector', 'connector2': 'CargoConnector', 'instance1':'cargo', 'instance2':'cargo_case'},
	{'connector1': 'ORIENTCONN', 'connector2': 'Orient_Connector', 'instance1':'Orient', 'instance2':'main_hub'}
	]
	if design.uav:
		if not remove_boilerplate:
			for connection in boiler_plate_connections:
				output_string += ',\n'
				output_string += '{{'\
				'"connector1": "{}",\n'\
				'"connector2": "{}",\n'\
				'"instance1": "{}",\n'\
				'"instance2": "{}"\n'\
				'}}'.format(connection['connector1'], connection['connector2'], connection['instance1'], connection['instance2'])
				output_string += ',\n'
				output_string += '{{'\
				'"connector1": "{}",\n'\
				'"connector2": "{}",\n'\
				'"instance1": "{}",\n'\
				'"instance2": "{}"\n'\
				'}}'.format(connection['connector2'], connection['connector1'], connection['instance2'], connection['instance1'])

	
	output_string += "],\n"
	output_string += '"design": "Generated_{}",\n'.format(design_num)
	output_string += '"instances": [\n '
	for key in design.parts.keys():
		if output_string[-1] == '}':	
			output_string += ',\n'
		if design.parts[key].part_type in ['p','h']:
			motor_model_name = uav_type_models['m'] if design.uav else 'MAGiDRIVE150'
			if design.uav:
				flange_model = uav_type_models['fl']
				tube_model = uav_type_models['t']


				#Add flange
				output_string += '{\n'\
				'"assignment": {\n'
				param_string, new_params = generate_instance_params('fl' + key[1:], 'fl')
				output_string += param_string
				parameters = parameters + new_params
				output_string += '}},\n'\
				'"model" : "{}",\n'\
				'"name": "{}"\n'\
				'}},'.format(flange_model,'fl' + design.parts[key].pid[1:])

				#Add prop tube
				# output_string += '{\n'\
				# '"assignment": {\n'
				# param_string, new_params = generate_instance_params('pt' + key[1:], 'pt')
				# output_string += param_string
				# parameters.extend(new_params)
				# output_string += '}},\n'\
				# '"model" : "{}",\n'\
				# '"name": "{}"\n'\
				# '}},'.format(tube_model,'pt' + design.parts[key].pid[1:])

				output_string += '{\n'\
				'"assignment": {\n'
				param_string, new_params = generate_instance_params('m' + key[1:], 'm')
				output_string += param_string
				parameters.extend(new_params)
				output_string += '}},\n'\
				'"model" : "{}",\n'\
				'"name": "{}"\n'\
				'}},'.format(motor_model_name,'m' + design.parts[key].pid[1:])


		# if design.parts[key].part_type == 'f':
		# 	model_name = 'capsule_fuselage' if design.uav else "FUSE_SPHERE_CYL_CONE"
		# 	if design.uav:
		# 		output_string += '{{\n'\
		# 		'"assignment": {{\n'\
		# 		'"FLOOR_HEIGHT": "FuselageFloorHeight",\n'\
		# 		'"LENGTH": "FuselageLength",\n'\
		# 		'"MIDDLE_LENGTH": "FuselageMiddleLength",\n'\
		# 		'"PORT_THICKNESS": "FuselagePortThickness",\n'\
		# 		'"SEAT_1_FB": "FuselageSeatFB",\n'\
		# 		'"SEAT_1_LR": "FuselageSeat1LR",\n'\
		# 		'"SEAT_2_FB": "FuselageSeatFB",\n'\
		# 		'"SEAT_2_LR": "FuselageSeat2LR",\n'\
		# 		'"SPHERE_DIAMETER": "FuselageSphereDiameter",\n'\
		# 		'"BOTTOM_CONNECTOR_OFFSET_LENGTH": "fuselage_BOTTOM_CONNECTOR_OFFSET_LENGTH",\n'\
		# 		'"BOTTOM_CONNECTOR_OFFSET_WIDTH": "fuselage_BOTTOM_CONNECTOR_OFFSET_WIDTH",\n'\
		# 		'"BOTTOM_CONNECTOR_ROTATION": "fuselage_BOTTOM_CONNECTOR_ROTATION",\n'\
		# 		'"FLOOR_CONNECTOR_1_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_1_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_1_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_1_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_2_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_2_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_2_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_2_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_3_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_3_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_3_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_3_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_4_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_4_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_4_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_4_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_5_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_5_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_5_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_5_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_6_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_6_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_6_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_6_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_7_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_7_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_7_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_7_DISP_WIDTH",\n'\
		# 		'"FLOOR_CONNECTOR_8_DISP_LENGTH": "fuselage_FLOOR_CONNECTOR_8_DISP_LENGTH",\n'\
		# 		'"FLOOR_CONNECTOR_8_DISP_WIDTH": "fuselage_FLOOR_CONNECTOR_8_DISP_WIDTH",\n'\
		# 		'"FLOOR_HEIGHT": "fuselage_FLOOR_HEIGHT",\n'\
		# 		'"FUSE_CYL_LENGTH": "fuselage_FUSE_CYL_LENGTH",\n'\
		# 		'"HORZ_DIAMETER": "fuselage_HORZ_DIAMETER",\n'\
		# 		'"VERT_DIAMETER": "fuselage_VERT_DIAMETER",\n'\
		# 		'"TAIL_DIAMETER": "FuselageTailDiameter"\n'\
		# 		'}},\n'\
		# 		'"model" : "{}",\n'\
		# 		'"name": "{}"\n'\
		# 		'}}'.format(model_name,'fuselage')
		# 	else:
		# 		output_string += '{{\n'\
		# 		'"assignment": {{\n'\
		# 		'"FLOOR_HEIGHT": "fuse_floor",\n'\
		# 		'"BOTTOM_CONNECTOR_ROTATION": "BodyRotAngle",\n'\
		# 		'"HORZ_DIAMETER": "fuse_width",\n'\
		# 		'"TUBE_LENGTH": "Vertical_Tube_Length",\n'\
		# 		'"VERT_DIAMETER": "fuse_height"\n'\
		# 		'}},\n'\
		# 		'"model" : "{}",\n'\
		# 		'"name": "{}"\n'\
		# 		'}}'.format(model_name,design.parts[key].pid)
		# elif design.parts[key].part_type == 'cg':
		# 	model_name = 'CargoCase'
		# 	instance_name = 'cargo_case'
		# 	output_string += '{{\n'\
		# 		'"assignment": {{\n'\
		# 		'"Rotation": "cargo_case_Rotation"\n'\
		# 		'}},\n'\
		# 		'"model" : "{}",\n'\
		# 		'"name": "{}"\n'\
		# 		'}}'.format(model_name,instance_name)
		# else:

		model_name = uav_type_models[design.parts[key].part_type]
		output_string += '{\n'\
		'"assignment": {\n'
		param_string, new_params = generate_instance_params(key, design.parts[key].part_type)
		output_string += param_string
		parameters.extend(new_params)
		output_string += '}},\n'\
		'"model" : "{}",\n'\
		'"name": "{}"\n'\
		'}},'.format(model_name,design.parts[key].pid)



		if design.parts[key].part_type == 'w':
			servo_name = 'servo' + key[1:]
			servo_model = 'Hitec_HS_40'
			output_string += '{{\n'\
			'"assignment": {{}},\n'\
			'"model" : "{}",\n'\
			'"name": "{}"\n'\
			'}}'.format(servo_model,servo_name)


	if design.uav:
		if not remove_boilerplate:
			boiler_plate_instances = [
			{'assignment': [('ROTATION', 'Autopilot_ROTATION')], 'model': 'Autopilot', 'name': 'Autopilot'},
			{'assignment': [], 'model': 'BatteryController', 'name': 'BatteryController'},
			{'assignment': [], 'model': 'TurnigyGraphene6000mAh6S75C', 'name': 'Main_Battery'},
			{'assignment': [], 'model': 'ControlBox', 'name': 'ControlBox'},
			# {'assignment': [('ROTATION', 'Battery_1_ROTATION')], 'model': 'TurnigyGraphene6000mAh6S75C', 'name': 'Battery_1'},
			# {'assignment': [('ROTATION', 'Battery_2_ROTATION')], 'model': 'TurnigyGraphene6000mAh6S75C', 'name': 'Battery_2'},
			{'assignment': [('ROTATION', 'Current_ROTATION')], 'model': 'Current', 'name': 'Current'},
			{'assignment': [('ROTATION', 'GPS_ROTATION')], 'model': 'GPS', 'name': 'GPS'},
			{'assignment': [('Z_ANGLE', 'Orient_Z_ANGLE')], 'model': 'Orient', 'name': 'Orient'},
			{'assignment': [('ROTATION', 'RpmTemp_ROTATION')], 'model': 'RpmTemp', 'name': 'RpmTemp'},
			{'assignment': [('ROTATION', 'Variometer_ROTATION')], 'model': 'Variometer', 'name': 'Variometer'},
			{'assignment': [('ROTATION', 'Voltage_ROTATION')], 'model': 'Voltage', 'name': 'Voltage'},
			{'assignment': [('Rotation', 'cargo_case_Rotation')], 'model': 'CargoCase', 'name': 'cargo_case'},
			{'assignment': [('WEIGHT', 'cargo_WEIGHT')], 'model': 'Cargo', 'name': 'cargo'}]

			for instance in boiler_plate_instances:
				output_string += '{\n'\
				'"assignment": {\n'
				for assignment in instance['assignment']:
					output_string += '"{}" : "{}",'.format(assignment[0], assignment[1])

				output_string = output_string[:-1]

				output_string += '}},\n'\
				'"model" : "{}",\n'\
				'"name": "{}"\n'\
				'}},'.format(instance['model'], instance['name'])	

			output_string = output_string[:-1]

	output_string += "],"
	if design.uav:
		control_channel_counter = 2
		output_string += '"parameters":{\n'
		for param in parameters:


			cleaned_param = param[1] if param[2] else param[0][param[0].index("_") + 1:] 
			if param[1][:4] == 'main':
				cleaned_param = param[1][9:]

			if cleaned_param == "CONTROL_CHANNEL":
				output_string += '"{}" : "{}",\n'.format(param[0], '{}'.format(str(control_channel_counter)))
				control_channel_counter += 1
			elif cleaned_param == "Length":
				pid = param[0][:param[0].index("_")]
				base_part = design.parts[design.parts[pid].connections["BaseConnection"]]
				end_part = design.parts[design.parts[pid].connections["EndConnection"]]
				if (base_part.part_type in ['bc', 'c']) and (end_part.part_type in ['bc', 'c']):
					if (base_part.hub_type in ['main', 'fuselage']) and (end_part.hub_type in ['main', 'fuselage']):
						output_string += '"{}" : "{}",\n'.format(param[0], 350)
				else:
					output_string += '"{}" : "{}",\n'.format(param[0], default_value_dict[cleaned_param])

			elif cleaned_param == "SPAN":
				pid = param[0][:param[0].index("_")]
				base_part = design.parts[pid]
				if (base_part.part_type in ['l']):
					output_string += '"{}" : "{}",\n'.format(param[0], 150)
				else:
					output_string += '"{}" : "{}",\n'.format(param[0], default_value_dict[cleaned_param])

			elif cleaned_param == "BASE_ROT":
				pid = param[0][:param[0].index("_")] 
				if design.parts[pid].connections["BaseConnection"][0] in ['w','l']:
					origin_hub = design.parts[design.parts[pid].connections["EndConnection"]]
					origin_connection = None
					for connection in origin_hub.connections.keys():
						if origin_hub.connections[connection] == pid:
							origin_connection = connection
					if origin_connection in ['rear', 'left']:
						output_string += '"{}" : "{}",\n'.format(param[0], 90)
					elif origin_connection in ['front', 'right']:
						output_string += '"{}" : "{}",\n'.format(param[0], 270)
					elif origin_connection in ['top']:
						output_string += '"{}" : "{}",\n'.format(param[0], 270)
					elif origin_connection in ['bottom']:
						output_string += '"{}" : "{}",\n'.format(param[0], 90)
			elif cleaned_param in default_value_dict.keys():
				output_string += '"{}" : "{}",\n'.format(param[0], default_value_dict[cleaned_param])
			else:
				output_string += '"{}" : "{}",\n'.format(param[0], param[1])
		output_string = output_string[:-2]
		output_string += '}}]'
	
	else:
	
		output_string += '"parameters":{\n'
		for param in parameters:

			if param[0] in default_value_dict.keys():

				output_string += '"{}" : "{}",\n'.format(param[0], default_value_dict[param[0]])
			else:
				output_string += '"{}" : "{}",\n'.format(param[0], param[1])


		output_string = output_string[:-1]
		output_string += '}}]'			
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


	#TODO: add a complex bounding box for non_parallel wings. Worst case scenario: set of consecutive, contiguous, cuboid bounding boxes.
	#Theta should be in radians
	def calculate_non_parallel_wing_bounding_box(theta, x_width, y_height, z_depth):
		functional_x_width = math.cos(theta)*x_width + math.sin(theta)*y_height
		functional_y_height = math.sin(theta)*x_width + math.cos(theta)*y_height
		return (functional_x_width,functional_y_height,z_depth)

	def add_connection(self, src, dst):
		self.connections[src] = dst


class connector(part):
	def __init__(self, pid, centroid = [0,0,0], buffer_connector = False, uav = False, hub_type = 'part'):
		part.__init__(self, pid, part_type = 'c')
		self.centroid = centroid
		self.buffer_connector = buffer_connector
		self.hub_type = hub_type
		if not uav:
			self.connections = {'front': None, 'rear' : None, 'top': None, 'bottom': None, 'left': None, 'right': None}
		else:
			if hub_type == 'main':
				self.connections = {'front': None, 'rear' : None, 'top': None, 'left': None, 'right': None}
			elif hub_type == 'buffer':
				self.connections = {'front': None, 'rear' : None, 'top': None, 'bottom': None}
			elif hub_type == 'part':
				self.connections = {'front': None, 'rear' : None, 'top': None, 'bottom': None, 'right': None}
			elif hub_type == 'fuselage':
				self.connections = {'front': None, 'rear' : None, 'top': None, 'bottom': None, 'left': None, 'right': None}


class tube(part):
	def __init__(self, pid, centroid = [0,0,0]):
		part.__init__(self, pid, part_type = 't')
		# self.centroid = centroid
		# self.buffer_connector = buffer_connector
		self.connections = {'front': None, 'rear' : None}


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
	def __init__(self, clusters = [], uav = False):
		self.bounding_boxes = []
		self.parts = {}
		self.part_id_count = 0
		self.tube_id_count = 0
		self.part_id_count = 0
		self.uav = uav
		self.initial_connector = connector("c" + str(self.part_id_count))
		self.add_part(self.initial_connector)
		self.part_id_count += 1
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

	#Simultaneously check for conflicts and add new bounding box
	def add_bounding_box(self, new_box):
		for bounding_box1 in self.bounding_boxes:
			for bounding_box2 in self.bounding_boxes:
				if self.check_interference(bounding_box1,bounding_box2):
					return False
		self.bounding_boxes.append(new_box)
		return True

	#Add a part, calls bounding box check
	def add_part(self, part):
		if not part.part_type in ['c','t']:
			if self.add_bounding_box(part.bounding_box):
				self.parts[part.pid] = part
			else:
				print("Return value:" + str(self.add_bounding_box(part.bounding_box)))
				print("Collision detected, failed to add part")
				print("PID:" + part.pid)
				print("centroid:")
				print(part.centroid)
				self.print_parts_and_centroids()
				sys.exit()
		else:
			self.parts[part.pid] = part

	def make_connection(self, src_pid, src_conn, dst_pid, dst_conn):
		# If we are using UAV style connections, utilize a tube to connect the two parts
		if self.uav and not (self.parts[dst_pid].part_type in ['cg','f']):
			connecting_tube = tube(pid = 't' + str(self.tube_id_count))
			self.tube_id_count += 1
			self.parts[src_pid].connections[src_conn] = connecting_tube.pid
			connecting_tube.connections["BaseConnection"] = src_pid
			self.parts[dst_pid].connections[dst_conn] = connecting_tube.pid
			connecting_tube.connections["EndConnection"] = dst_pid
			self.add_part(connecting_tube)
		# If we are using UAM, simply connect the two parts
		else:
			self.parts[src_pid].connections[src_conn] = dst_pid
			self.parts[dst_pid].connections[dst_conn] = src_pid


	def print_parts_and_centroids(self):
		for key in self.parts.keys():
			part = self.parts[key]
			print(part.pid)	
			part.bounding_box.print_bounds()

	def z_bound_check(self, part, z_min, z_max):
		if part.bounding_box.max_z > z_max:
			z_max = part.bounding_box.max_z
		if part.bounding_box.min_z > z_min:
			z_min = part.bounding_box.min_z
		return z_min, z_max

	def get_buffer_connectors(self, z = None, y = None):
		buffer_connectors = []
		for key in self.parts.keys():
			part = self.parts[key]
			if part.part_type in ['bc','c']:
				if part.buffer_connector:
					if z:
						if y:
							if part.centroid[1] == y and part.centroid[2] == z:
								buffer_connectors.append(part)
						else:
							if part.centroid[2] == z:
								buffer_connectors.append(part)
					else:
						buffer_connectors.append(part)

		return buffer_connectors 

	def find_valid_buffer(self, z_bound, minimum_position, direction, y_bound = None):
		possible_connectors = self.get_buffer_connectors(z = z_bound, y = y_bound)
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
		# print(schema)
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
		index = math.floor(len(self.clusters)/2)
		alternator = -1
		offset = 0
		i = 0
		while i < len(self.clusters):
			new_clusters.append(self.clusters[index + (offset * alternator)])
			if alternator == -1:
				offset += 1
			alternator *= -1
			i += 1

		# for cluster in self.clusters:
		# 	if 'f' in cluster:
		# 		new_clusters = [cluster] + new_clusters
		# 	else:
		# 		new_clusters.append(cluster)

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
		connector = self.frontmost_connector
		print("placing cluster: ")
		print(cluster)
		cursor, z_min, z_max, return_connector = self.place_cluster_pos_lock(cluster, cursor, connector, direction)
		temporary_z_buffer = 10
		rear_cursor[2] += z_min
		rear_cursor[2] -= temporary_z_buffer
		front_cursor[2] += z_max
		front_cursor[2] += temporary_z_buffer


		#For each cluster, identify a connector to branch off of and a cursor to use. Update cursors from maxes of last iteration and place
		temporary_z_buffer = 10
		for cluster  in self.clusters[1:]:
			print("placing cluster: ")
			print(cluster)
			if alternator == -1:
				connector = self.frontmost_connector
				rear_cursor[2] += z_min
				rear_cursor[2] -= temporary_z_buffer
				cursor = front_cursor
				direction = "front"
				cursor, z_min, z_max, self.frontmost_connector = self.place_cluster_pos_lock(cluster, cursor, connector, direction)
			else:
				front_cursor[2] += z_max
				front_cursor[2] += temporary_z_buffer
				connector = self.rearmost_connector
				cursor = rear_cursor
				direction = "rear"
				cursor, z_min, z_max, self.rearmost_connector = self.place_cluster_pos_lock(cluster, cursor, connector, direction)
			

			alternator *= -1

	#Place clusters where parts' centroids have the same z value

	#Account for number of separate connector clusters
	def place_cluster_pos_lock(self, cluster, cursor, origin_connector, direction = "front"):

		#Count subclusters and track where they start/end
		base_connector = None
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
				# schema = 'even' if (subcluster_count % 2 == 0) else 'odd'
			else:

				i += 1

		i = 0
		subcluster_index = 0
		subcluster_processing_order = []
		subcluster_boundary_index = len(subclusters)//2
		subcluster_boundary_offset = 0
		subcluster_boundary_alternator = 1
		j = 0 
		while j < len(subclusters):
			subcluster_processing_order.append(subclusters[
				subcluster_boundary_index + (subcluster_boundary_offset * 
					subcluster_boundary_alternator)])
			subcluster_boundary_alternator *= -1
			if j % 2 == 0:
				subcluster_boundary_offset += 1
			j += 1


		new_tokens = []

		buffer_size = 1
		
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
			fuselage_id = 'fuselage'
			# 'f' + str(self.part_id_count)
			self.part_id_count += 1
			

			# differentiate uav/uam style interpretation
			if not self.uav:
				new_part = part(fuselage_id ,centroid=cursor, part_type='f', x_width=fuselage_dimensions["x_width"], y_height=fuselage_dimensions["y_height"], z_depth=fuselage_dimensions["z_depth"])
				self.add_part(new_part)
				# Track min and max z for incrementation (this will be repeated without comment)
				z_min, z_max = self.z_bound_check(new_part, z_min, z_max)
				# connect single initial connector to front fuselage, and connect rear of connector to front of fuselage
				self.frontmost_connector.connections["rear"] = fuselage_id
				self.parts[fuselage_id].connections['front'] = self.frontmost_connector.pid

				# create rear connector, connect front of rear connector to rear of fuselage
				new_connector = connector('c' + str(self.part_id_count))
				new_connector.connections["front"] = fuselage_id
				self.parts[fuselage_id].connections['rear'] = new_connector.pid
				self.part_id_count += 1
				self.rearmost_connector = new_connector
				self.add_part(new_connector)

			else:
				temp_cursor = [x for x in cursor]
				base_hub = connector('main_hub', cursor, uav = True, hub_type = 'fuselage')
				self.add_part(base_hub)
				temp_cursor[1] += fuselage_dimensions["y_height"]/2
				fuselage = part(fuselage_id ,centroid=temp_cursor, part_type='f', x_width=fuselage_dimensions["x_width"], y_height=fuselage_dimensions["y_height"], z_depth=fuselage_dimensions["z_depth"])
				self.add_part(fuselage)
				temp_cursor[1] -= fuselage_dimensions["y_height"]/2
				cargo_dimensions = part_dimensions['cg']
				temp_cursor[1] -= cargo_dimensions["y_height"]/2
				cargo = part('cargo_case', centroid = temp_cursor, part_type = 'cg', x_width=cargo_dimensions["x_width"], y_height=cargo_dimensions["y_height"], z_depth=cargo_dimensions["z_depth"])
				self.add_part(cargo)
				#disable
				self.make_connection(base_hub.pid, 'top', fuselage.pid, 'BottomConnectore') #RUIN BOTTOM CONNECTOR NAME TO REMOVE FUSELAGE
				self.make_connection(base_hub.pid, 'bottom', cargo.pid, 'top')
				self.frontmost_connector = base_hub
				self.rearmost_connector = base_hub




			# If there are two wings
			if w_count == 2:
				if not self.uav:

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
				else:
					temp_cursor = [x for x in cursor]
					dimensions = part_dimensions['w']
					temp_cursor[0] -= dimensions['x_width'] * 2
					new_wing = part('w' + str(self.part_id_count), part_type = 'w', centroid= temp_cursor,  x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count += 1
					self.add_part(new_wing)
					self.make_connection(new_wing.pid, "Wing_Tube_Connector", base_hub.pid, "left")
					temp_cursor[0] += dimensions['x_width']
					new_wing = part('w' + str(self.part_id_count), centroid = temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count += 1
					self.add_part(new_wing)
					self.make_connection(new_wing.pid, "Wing_Tube_Connector", base_hub.pid, "right")


			# If there are 4 wings and a fuselage
			if w_count == 4:
				# Create temporary cursor for placing parts. Start on top of fuselage
				temp_cursor = [cursor[0], cursor[1]+ fuselage_dimensions["y_height"]/2, cursor[2]]

				#Create a connector flush with the top of the fuselage, connect it to top of fuselage
				new_connector = connector('c' + str(self.part_id_count))
				new_connector.connections['bottom'] = fuselage_id
				self.parts[fuselage_id].connections['top'] = new_connector.pid
				self.add_part(new_connector)
				self.part_id_count += 1

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
				new_connector = connector('c' + str(self.part_id_count))
				new_connector.connections['top'] = fuselage_id
				self.parts[fuselage_id].connections['bottom'] = new_connector.pid
				self.add_part(new_connector)
				self.part_id_count += 1

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

		elif w_count == 2:
			base_connector = connector('c' + str(self.part_id_count), buffer_connector = True, hub_type = 'main')
			self.part_id_count += 1
			self.add_part(base_connector)
			
			# origin_connector.connections[direction] = base_connector.pid
			if direction == 'front':
				#right
				self.make_connection(origin_connector.pid, direction, base_connector.pid, "rear")
			else:
				#left
				self.make_connection(origin_connector.pid, direction, base_connector.pid, "front")

			temp_cursor = [x for x in cursor]
			dimensions = part_dimensions['w']

			temp_cursor[0] -= dimensions['x_width']/2
			first_wing = part('w' + str(self.part_id_count), centroid=temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
			self.part_id_count += 1
			self.add_part(first_wing)
			self.make_connection(first_wing.pid, 'Wing_Tube_Connector', base_connector.pid, 'left')

			temp_cursor[0] += dimensions['x_width']
			second_wing = part('w' + str(self.part_id_count), centroid=temp_cursor, part_type = 'w', x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
			self.part_id_count += 1
			self.add_part(second_wing)
			self.make_connection(second_wing.pid, 'Wing_Tube_Connector', base_connector.pid, 'right')



			pass
		# elif 'l' in tokens:
		# 	pass
		else:
			offset = 0
			alternator = 1
			temp_cursor = [x for x in cursor]
			string_index = len(tokens)//2
			centered = len(tokens) % 2 == 1

			# Add perpendicular connector to start attatching parts
			# TODO: fix issue with utilizing f + non w
			base_connector = connector('c' + str(self.part_id_count), buffer_connector = True, hub_type = 'main')
			self.part_id_count += 1
			self.add_part(base_connector)
			
			# origin_connector.connections[direction] = base_connector.pid
			if direction == 'front':
				#right
				self.make_connection(origin_connector.pid, direction, base_connector.pid, "rear")
			else:
				#left
				self.make_connection(origin_connector.pid, direction, base_connector.pid, "front")
			
			leftmost_connector = base_connector
			rightmost_connector = base_connector

			i = 0

			while i < len(tokens):
				current_token_index = string_index + (offset * alternator)

				print("placing token: "+ tokens[current_token_index])
				print(current_token_index)

				dimensions = part_dimensions[tokens[current_token_index]]
				#The first part gets centered on the cursor, the following are placed either to the left or right
				if i == 0 and centered:

					# Add the first, centered part
					new_part = part(tokens[current_token_index] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[current_token_index], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count +=1
					self.add_part(new_part)

					# Update the left and right most positions
					rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
					leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]

					#Update the cursor position
					temp_cursor = leftmost

					#Connect the base to the base connector (different for horizontal and vertical)
					if new_part.part_type == 'h':
						#right
						self.make_connection(new_part.pid, "baseplate", base_connector.pid, 'front')
					elif new_part.part_type == 'l':
						self.make_connection(new_part.pid, "Wing_Tube_Connector", base_connector.pid, "top")
					else:
						self.make_connection(new_part.pid, "baseplate", base_connector.pid, "top")

					# Increment the offset
					offset += 1
					alternator = -1

				else:

					# Move the cursor to the new centroid and add the current part there
					temp_cursor = [temp_cursor[0] + ((dimensions["x_width"] + buffer_size)/2 * alternator), temp_cursor[1], temp_cursor[2]]
					new_part = part(tokens[current_token_index] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[current_token_index], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
					self.part_id_count +=1

					# Add a buffer connector
					buffer_connector = connector('bc' + str(self.part_id_count),centroid = temp_cursor, buffer_connector = True)
					self.add_part(buffer_connector)
					if alternator == -1:

						# Attach buffer connecter, create and attach new connector to hold part
						#front, rear
						self.make_connection(leftmost_connector.pid, 'left', buffer_connector.pid, 'right')
						self.part_id_count += 1
						new_connector = connector('c' + str(self.part_id_count))
						self.part_id_count += 1
						self.add_part(new_connector)
						# buffer_connector.connections['front'] = new_connector.pid
						# new_connector.connections['rear'] = buffer_connector.pid
						#rear, front
						self.make_connection(new_connector.pid, 'right', buffer_connector.pid, 'left')
						

						# Update leftmost position and connector
						leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
						leftmost_connector = new_connector
						temp_cursor = [x for x in rightmost]
					else:

						# Attach buffer connecter, create and attach new connector to hold part
						self.make_connection(rightmost_connector.pid, 'right', buffer_connector.pid, 'left')
						self.part_id_count += 1
						new_connector = connector('c' + str(self.part_id_count))
						self.part_id_count += 1
						self.add_part(new_connector)
						self.make_connection(new_connector.pid, 'left', buffer_connector.pid, 'right')
						

						# Update rightmost position and connector
						rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
						rightmost_connector = new_connector
						temp_cursor = [x for x in leftmost]
						offset += 1
					# Attach part and new connector
					self.add_part(new_part)
					if new_part.part_type == 'h':
						# placement = 'right' if direction == "front"
						#used to be direction
						self.make_connection(new_part.pid, 'baseplate', new_connector.pid, 'front')
						# new_connector.connections[direction] = new_part.pid
					elif new_part.part_type == 'l':
						self.make_connection(new_part.pid, "Wing_Tube_Connector", new_connector.pid, "top")
					else:
						self.make_connection(new_part.pid, 'baseplate', new_connector.pid, 'top')
					
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

		 
		# print(subcluster_processing_order)
		
		i = 0
		# Process subclusters
		for i in range(len(subcluster_processing_order)):
		# for subcluster in subcluster_processing_order:
			# detemine which quadrant the branching connector will be placed in
			quadrant = self.determine_quadrant(part_schema, i, len(subcluster_processing_order)%2 == 1)

			# Determine the direction of cursor movement, as well as the minimum distance of the buffer connector
			direction = -1 if quadrant in [0,2] else 1
			# If we have an odd subcluster # and we're at the first subcluster, we'll be placing using the middle connector
			if i == 0 and len(subcluster_processing_order) % 2 == 1:
				centered = True
				minimum_position = 0
			else:
				#if not, find out the max possible x_size of the cluster
				x_sum = 0
				for token in subcluster_processing_order[i]:
					x_width = part_dimensions[token]["x_width"]
					x_sum += x_width

				
				x_bound = bounds[quadrant]
				minimum_position = x_bound + ((x_width/2) * direction)

			# Try to find a valid buffer connector
			buffer_connector = self.find_valid_buffer(cursor[2], minimum_position, direction, y_bound = cursor[1])

			# If a valid buffer connector does not exist, add a new one and connect it to the appropriate edge connector
			if not buffer_connector:
				new_buffer = connector('bc' + str(self.part_id_count), buffer_connector = True)
				self.part_id_count += 1

				if direction == 1:
					new_centroid = [x for x in rightmost_connector.centroid]
					new_centroid[0] = minimum_position + 1
					new_buffer.centroid = new_centroid
					self.add_part(new_buffer)
					# self.parts[rightmost_connector.pid].connections['right'] = new_buffer.pid
					self.make_connection(rightmost_connector.pid, 'right', new_buffer.pid, 'left')
					rightmost_connector = new_buffer

				else:
					new_centroid = [x for x in leftmost_connector.centroid]
					new_centroid[0] = minimum_position - 1
					new_buffer.centroid = new_centroid
					self.add_part(new_buffer)
					# self.parts[leftmost_connector.pid].connections['front'] = new_buffer.pid
					self.make_connection(leftmost_connector.pid, 'left', new_buffer.pid, 'right')
					leftmost_connector = new_buffer
				buffer_connector = new_buffer


			# Place the subcluster using the buffer as a connection point, get new left/right bounds
			sub_z_min, sub_z_max, bound = self.place_cluster_separate_connector(subcluster_processing_order[i], 
				temp_cursor, part_schema = part_schema, subcluster_schema = subcluster_schema, subcluster_index = i, quadrant = quadrant,
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

		return_connector = base_connector if base_connector else base_hub	
		return temp_cursor, z_max, z_min, return_connector


	#Place clusters that are on a separate connector from the principal connector
	def place_cluster_separate_connector(self, tokens, cursor, origin_connector, subcluster_schema = 'Grouped', subcluster_index = 0, part_schema = "Grouped", deviation = 10, z_max = 0, quadrant = 0):

		alternator = -1
		offset = 0
		directions = [-1,1,-1,1]
		y_directions = [1,1,-1,-1]
		vertical_connection = ["top", "top", "bottom", "bottom"]
		rising_connection = ["front", "front", "rear", "rear"]
		rising_connector = connector('c' + str(self.part_id_count))
		self.part_id_count += 1
		self.add_part(rising_connector)
		# rising_connector.connections["rear"] = origin_connector.pid
		# self.parts[origin_connector.pid].connections[vertical_connection[quadrant]] = rising_connector.pid
		# self.make_connection(origin_connector.pid, vertical_connection[quadrant], rising_connector.pid, 'rear')
		self.make_connection(origin_connector.pid, vertical_connection[quadrant], rising_connector.pid, vertical_connection[(quadrant+2)%2])

		temp_cursor = [x for x in cursor]
		string_index = len(tokens)//2
		centered = len(tokens) % 2 == 1

		# Add perpendicular connector to start attatching parts
		# TODO: fix issue with utilizing f + non w
		base_connector = rising_connector
		# base_connector = connector('c' + str(self.part_id_count))
		# self.part_id_count += 1
		# self.add_part(base_connector)
		# self.make_connection(rising_connector.pid, rising_connection[quadrant], base_connector.pid, vertical_connection[(quadrant + 2) % 4])
		leftmost_connector = base_connector
		rightmost_connector = base_connector
		leftmost = [x for x in cursor]
		rightmost = [x for x in cursor]


		i = 0

		while i < len(tokens):
			current_token_index = string_index + (offset * alternator)
			dimensions = part_dimensions[tokens[current_token_index]]

			print("placing token: "+ tokens[current_token_index])
			print(current_token_index)

			#The first part gets centered on the cursor, the following are placed either to the left or right
			if i == 0 and centered:

				# Add the first, centered part
				new_part = part(tokens[current_token_index] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[current_token_index], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				self.part_id_count +=1
				self.add_part(new_part)

				# Update the left and right most positions
				rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
				leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]

				#Update the cursor position
				temp_cursor = leftmost

				#Connect the base to the base connector (different for horizontal and vertical)
				# new_part.connections["baseplate"] = base_connector.pid
				if new_part.part_type == 'h':
					self.make_connection(new_part.pid, 'baseplate', base_connector.pid, 'front')
					# base_connector.connections['right'] = new_part.pid
				elif new_part.part_type == 'l':
						self.make_connection(new_part.pid, "Wing_Tube_Connector", base_connector.pid, vertical_connection[quadrant]) #"top"
				else:
					self.make_connection(new_part.pid, 'baseplate', base_connector.pid, vertical_connection[quadrant]) #top
					# base_connector.connections['top'] = new_part.pid

				# Increment the offset
				offset += 1

			else:

				# Move the cursor to the new centroid and add the current part there
				temp_cursor = [temp_cursor[0] + (dimensions["x_width"]/2 * alternator), temp_cursor[1], temp_cursor[2]]
				new_part = part(tokens[current_token_index] + str(self.part_id_count), centroid=temp_cursor, part_type = tokens[current_token_index], x_width=dimensions["x_width"], y_height=dimensions["y_height"], z_depth=dimensions["z_depth"])
				self.part_id_count +=1
				self.add_part(new_part)

				# Add a buffer connector
				buffer_connector = connector('bc' + str(self.part_id_count),centroid = temp_cursor, buffer_connector = True)
				self.part_id_count += 1
				self.add_part(buffer_connector)
				if alternator == -1:

					# Attach buffer connecter, create and attach new connector to hold part
					#front, rear
					self.make_connection(leftmost_connector.pid, 'left', buffer_connector.pid, 'right')
					self.part_id_count += 1
					new_connector = connector('c' + str(self.part_id_count))
					self.part_id_count += 1
					self.add_part(new_connector)
					# buffer_connector.connections['front'] = new_connector.pid
					# new_connector.connections['rear'] = buffer_connector.pid
					#rear, front
					self.make_connection(new_connector.pid, 'right', buffer_connector.pid, 'left')
					

					# Update leftmost position and connector
					leftmost = [temp_cursor[0] - dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
					leftmost_connector = new_connector
					temp_cursor = [x for x in rightmost]
				else:

					# Attach buffer connecter, create and attach new connector to hold part
					self.make_connection(rightmost_connector.pid, 'right', buffer_connector.pid, 'left')
					new_connector = connector('c' + str(self.part_id_count))
					self.part_id_count += 1
					self.add_part(new_connector)
					self.make_connection(new_connector.pid, 'left', buffer_connector.pid, 'right')
					

					# Update rightmost position and connector
					rightmost = [temp_cursor[0] + dimensions["x_width"]/2, temp_cursor[1], temp_cursor[2]]
					rightmost_connector = new_connector
					temp_cursor = [x for x in leftmost]
					offset += 1
				# Attach part and new connector
				if new_part.part_type == 'h':
					self.make_connection(new_part.pid, 'baseplate', new_connector.pid, 'front')
				elif new_part.part_type == 'l':
						self.make_connection(new_part.pid, "Wing_Tube_Connector", new_connector.pid, vertical_connection[quadrant]) #"top"
				else:
					self.make_connection(new_part.pid, 'baseplate', new_connector.pid, vertical_connection[quadrant])  #"top"
				alternator *= -1
			if dimensions["z_depth"] > z_max:
				z_max = dimensions["z_depth"]
			i += 1

		return_values = [leftmost,rightmost,leftmost,rightmost]

		return return_values[quadrant]


	def print_parts(self, pids = True, connections = True):
		pid_list = []
		for key in self.parts.keys():
			pid_list.append(self.parts[key].pid)

			# print(self.parts[key])
		if pids:
			pid_list = sorted(pid_list)
			for pid in pid_list:
				print(pid)
		if connections:
			print(self.parts[key].connections)



if __name__ == '__main__':

	new_clusters = []
	# [['h','p','p','h'],['w','f','w'],['h','p','p','h']]
	# [['h','p','h'],['w','f','w'],['p'],['(','h','h',')']]
	#['(', 'p', 'p', ')','(', 'p', 'p', ')','(', 'p', 'p', ')']
	# [['h','p','h'],['w','f','w'],['h','p','h']]
	#['w','f','w'],
	#['p','p','p']
	#[['(', 'p', 'p', 'p', ')','(', 'p', 'p', ')','p','(', 'p', 'p', 'p', ')','p','(', 'p', 'p', ')','(', 'p', 'p', 'p', ')',],
	#['(', 'p', 'p', ')','p','p','p','(', 'p', 'p', ')']]
	#['(', 'p', 'p', ')', 'h', '(', 'p', 'p',')' ]
	#['h','p','h'],['w','f','w'],['h','p','h']
	# [['(', 'p', 'p', ')', 'h', 'h', '(', 'p', 'p',')' ],['w','f','w'],['(', 'p', 'p', ')', 'h', 'h','(', 'p', 'p',')' ]]

	parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
	parser.add_argument('-u', '--uav', default = "True")

	parser.add_argument('-f', '--filename', default = 'parser_input.txt')

	parser.add_argument('-s', '--string_input', default="True")

	parser.add_argument('-d', '--debug', action= "store_true")

	args = parser.parse_args()
	output_designs = []
	
	# Designs
	#[hh][pp][wfw][pp][hh]
	#[hhhh][ww][phhp][wfw][phhp][ww][hhhh]
	#
	if args.string_input == "True":
		file_name = args.filename
		source = open(file_name)
		lines = source.readlines()
		design_strings = []
		for line in lines:
			new_cluster_set = [x.strip('[') for x in line.split(']')][:-1]
			clusters = [[y for y in x] for x in new_cluster_set]
			design_strings.append(clusters)
	else:
		design_strings = [[['h','p','h'],['w','f','w'],['h','p','h']]]
	i = 0
	for design_string in design_strings:
		print(design_string)
		new_design = None
		new_design = design(clusters = design_string, uav = args.uav == "True")
		new_design.place_all_parts()
		# new_design.print_parts(connections = False)
		output = custom_encoder(new_design, i, remove_boilerplate = args.debug, )
		output_designs.append(output)
		new_design.parts = {}
		i += 1


	for i in range(len(output_designs)):
		output_file = open("generated_design{}.json".format(i), 'w')
		output_file.write(output_designs[i])
