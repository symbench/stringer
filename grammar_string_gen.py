"""
Grammar: EBNF
<part> :: = p | h | w | w'| f
<group> ::= {<group>}<part>{<group>}
<branching-group> ::= {<branching-group>}(<group>{<branching-group>}){<branching-group>}
<inner-group> ::= {<group>}{<branching-group>}<branching-group>{<branching-group>}{<group>} | {<group>}{<branching-group>}<group>{<branching-group>}{<group>}
<position-constrained-group> = [<inner-group>]
<cluster> ::= {<cluster>}<position-constrained-group>{<cluster>} | {<cluster>}<inner-group>{<cluster>}
<design> ::= {<cluster>}[w'fw']{<cluster>} | {<cluster>}[w'bw']{<cluster>}
Rules (to be formalized):
- h token terminates string on that side unless wrapped in () or connected to a wing
- minimum 2 parallel wings + fueselage
- symmetrical (orthoganal to principal axis)
- () necessitates branching from principal connector
- num of p/h/f tokens inside [] cannot be greater than num axes unless two of the tokens are w', in which case all tokens past num axes are considered attached to w' symmetrically, or they are contained within ()
- no w or w' inside ()
Token ordering process:
1. check for w'
2.
"""

import random
import argparse

def place_schema(tokens, s_type = "alternating", centerpiece = None):
	return_string = ""
	if centerpiece:
		if not (s_type == 'stacked') and centerpiece == 'h':
			return_string = '(h)'
			tokens['h'] -= 1
		if not (s_type == 'stacked') and centerpiece == 'p':
			return_string = 'p'
			tokens['p'] -= 1

	if s_type == 'alternating':
		while tokens['p'] + tokens['h'] > 1:
			if tokens['p'] > 0:
				return_string = 'p' + return_string + 'p'
				tokens['p'] -= 2
			if tokens['h'] > 0:
				return_string = 'h' + return_string + 'h'
				tokens['h'] -= 2
	elif s_type == "grouped":
		while tokens['h'] > 1:
			return_string = 'h' + return_string + 'h'
			tokens['h'] -= 2
		while tokens['p']:
			return_string = 'p' + return_string + 'p'
			tokens['p'] -= 2
	elif s_type == "stacked":
		num_branches = random.choice([1,2])
		if tokens['h'] >= tokens['p'] and tokens['p'] > 0:
			if num_branches == 2:
				branch_size = tokens['h']//2
				if tokens['p'] % 2 ==1:
					top_branch = "p"
					tokens['p'] -= 1
					while tokens['p'] > 1:
						top_branch = 'p' + top_branch + 'p'
						tokens['p'] -= 2
					top_branch = '(' + top_branch + ')'
					bottom_branch = ""
					if tokens['h'] % 2 == 1:
						bottom_branch = "h"
					while tokens['h'] > branch_size:
						bottom_branch = 'h' + bottom_branch + 'h'
						tokens['h'] -= 2
					bottom_branch = '(' + bottom_branch + ')'
					main_branch = ""
					while tokens['h'] > 1:
						main_branch = 'h' + main_branch + 'h'
						tokens['h'] -= 2
				else:
					top_branch = ""
					while tokens['h'] > branch_size:
						top_branch = 'h' + top_branch + 'h'
						tokens['h'] -= 2
					top_branch = '(' + top_branch + ')'
					bottom_branch = ""
					while tokens['h'] > 1:
						bottom_branch = 'h' + bottom_branch + 'h'
						tokens['h'] -= 2
					bottom_branch = '(' + bottom_branch + ')'
					main_branch = ""
					while tokens['p'] > 1:
						main_branch = 'p' + main_branch + 'p'
						tokens['p'] -= 2
				if bottom_branch == "()":
					return_string = top_branch + main_branch
				return_string = top_branch + main_branch + bottom_branch
			else:
				top_branch = ""
				if tokens['p'] % 2 ==1:
					top_branch = "p"
					tokens['p'] -= 1
				while tokens['p'] > 1:
					top_branch = 'p' + top_branch + 'p'
					tokens['p'] -= 2
				top_branch = '(' + top_branch + ')'
				main_branch = ""
				if tokens['h'] % 2 == 1:
					main_branch = "h"
					tokens['h'] -= 1

				while tokens['h'] > 1:
					main_branch = 'h' + main_branch + 'h'
					tokens['h'] -= 2
				return_string = top_branch + main_branch
			
		elif tokens['p'] > tokens['h'] and tokens['h'] > 0:
			
			if num_branches == 2:
				branch_size = tokens['p']//2
				top_branch = ""
				if tokens['p'] % 2 == 1:
					top_branch = "p"
					tokens['p'] -= 1
				while tokens['p'] > branch_size:
					top_branch = 'p' + top_branch + 'p'
					tokens['p'] -= 2
				top_branch = '(' + top_branch + ')'
				bottom_branch = ""
				if tokens['h'] % 2 == 1:
					bottom_branch = "h"
					tokens['h'] -= 1
					while tokens['h'] > 1:
						bottom_branch = 'h' + bottom_branch + 'h'
						tokens['h'] -= 2
					main_branch = ""
					while tokens['p'] > 1:
						main_branch = 'p' + main_branch + 'p'
						tokens['p'] -= 2
				else:
					while tokens['p'] > 1:
						bottom_branch = 'p' + bottom_branch + 'p'
						tokens['p'] -= 2
					bottom_branch = '(' + bottom_branch + ')'
					main_branch = ""
					if tokens['h'] % 2 == 1:
						main_branch = "h"
						tokens['h'] -= 1
					while tokens['h'] > 1:
						main_branch = 'h' + main_branch + 'h'
						tokens['h'] -= 2
				if bottom_branch == "()":
					return_string = top_branch + main_branch		
				return_string = top_branch + main_branch + bottom_branch
			else:
				top_branch = ""
				if tokens['p'] % 2 ==1:
					top_branch = "p"
					tokens['p'] -= 1
				while tokens['p'] > 1:
					top_branch = 'p' + top_branch + 'p'
					tokens['p'] -= 2
				top_branch = '(' + top_branch + ')'
				main_branch = ""
				if tokens['h'] % 2 == 1:
					main_branch = "h"
					tokens['h'] -= 1
				while tokens['h'] > 1:
					main_branch = 'h' + main_branch + 'h'
					tokens['h'] -= 2
				return_string = top_branch + main_branch
		elif tokens['h'] > 0 and tokens['p'] <= 0:
			if num_branches == 2:
				branch_size = tokens //3
				top_branch = ""
				if tokens['h'] % 2 == 1:
					top_branch = "h"
					tokens['h'] -= 1
				while tokens['h'] > branch_size * 2:
					top_branch = 'h' + top_branch + 'h'
					tokens['h'] -= 2
				top_branch = '(' + top_branch + ')'
				bottom_branch = ""
				while tokens['h'] >  branch_size:
					bottom_branch = 'h' + bottom_branch + 'h'
					tokens['h'] -= 2
				bottom_branch = '(' + bottom_branch + ')'
				main_branch = ""
				while tokens['h'] > 1:
					main_branch = 'h' + main_branch + 'h'
					tokens['h'] -= 2
				return_string = top_branch + main_branch + bottom_branch
			else:
				branch_size = tokens['p'] // 2
				top_branch = ""
				if tokens['h'] % 2 ==1:
					top_branch = "h"
					tokens['h'] -= 1
				while tokens['h'] > branch_size:
					top_branch = 'h' + top_branch + 'h'
					tokens['h'] -= 2
				top_branch = '(' + top_branch + ')'
				main_branch = ""
				if tokens['h'] % 2 == 1:
					main_branch = "h"
					tokens['h'] -= 1
				while tokens['h'] > 1:
					main_branch = 'h' + main_branch + 'h'
					tokens['h'] -= 2
				return_string = top_branch + main_branch
		elif tokens['p'] > 0 and tokens['h'] <= 0:
			if num_branches == 2:
				branch_size = tokens['p'] //3
				top_branch = ""
				if tokens['p'] % 2 == 1:
					top_branch = "p"
					tokens['p'] -= 1
				while tokens['p'] > branch_size * 2:
					top_branch = 'p' + top_branch + 'p'
					tokens['p'] -= 2
				top_branch = '(' + top_branch + ')'
				bottom_branch = ""
				if branch_size % 2 == 1:
					bottom_branch = "p"
					tokens['p'] -= 1
				while tokens['p'] >  branch_size:
					bottom_branch = 'p' + bottom_branch + 'p'
					tokens['p'] -= 2
				bottom_branch = '(' + bottom_branch + ')'
				main_branch = ""
				while tokens['p'] > 1:
					main_branch = 'p' + main_branch + 'p'
					tokens['p'] -= 2
				return_string = top_branch + main_branch + bottom_branch
			else:
				branch_size = tokens['p'] // 2
				top_branch = ""
				if tokens['p'] % 2 ==1:
					top_branch = "p"
					tokens['p'] -= 1
				while tokens['p'] > branch_size:
					top_branch = 'p' + top_branch + 'p'
					tokens['p'] -= 2
				top_branch = '(' + top_branch + ')'
				main_branch = ""
				while tokens['p'] > 1:
					main_branch = 'p' + main_branch + 'p'
					tokens['p'] -= 2
				return_string = top_branch + main_branch
	# print(s_type)
	if s_type == "stacked":
		# print(num_branches)
		pass
	return return_string











class uavStringGrammar:

    def __init__(self, length=9, symmetrical=True, num_axes=1, min_p=0, min_h=0, min_w=0, min_wp=2, min_f=1,
				fuselage_base=False, p_bias=0.2, h_bias=0.3, w_bias=0.1, wp_bias=0.2, branch_coefficient=0.3,
                grouping_coefficient=0.4, multiaxial_symmetry=False, mean_group_size=3, group_size_tolerance=2):

        self.grammar_params = {
            "terminal_tokens": ['p', 'h', 'w', 'w\'', 'f', 'b'],
            "minimum_tokens": {'p': 0, 'h': 0, 'w': 0, 'w\'': 2, 'f': 1, 'b': 0},
            "simplified_group_tokens": ['p', 'h', 'w', "w'"],
            "simplified_paren_tokens": ['p', 'h'],
            "token_biases": [0.2, 0.3, 0.1, 0.2, 0, 0],
            "non_terminal_tokens": {'(': ')', '[': ']'},
            "seed_groups": ['[hh]', '[ww]', '[pp]', '(pppppppppppp)', '(hh)'],
            "seed_clusters": ['[hh][ww][pp]', '[(pppppppppppp)(pppppppppppp)]', '[(hh)(hh)]', '[(hh)w\'fw\'(hh)]']
        }
        # self.min_length = min_length if (min_length >= 3) else 3
        # self.max_length = max_length if max_length > self.min_length else self.min_length
        self.length = length if length > 3 else 3
        self.symmetrical = symmetrical
        self.num_axes = num_axes if num_axes > 0 else 1
        self.grammar_params['minimum_tokens']['p'] = min_p
        self.grammar_params['minimum_tokens']['h'] = min_h
        self.grammar_params['minimum_tokens']['w'] = min_w
        if min_wp > self.grammar_params['minimum_tokens']['w\'']:
            self.grammar_params['minimum_tokens']['w\''] = min_wp
        if min_f > self.grammar_params['minimum_tokens']['f']:
            self.grammar_params['minimum_tokens']['f'] = min_f
        self.fuselage_base = fuselage_base
        self.p_bias = p_bias
        self.h_bias = h_bias
        self.w_bias = w_bias
        self.wp_bias = wp_bias
        self.branch_coefficient = branch_coefficient
        self.grouping_coefficient = grouping_coefficient
        self.multiaxial_symmetry = multiaxial_symmetry
        self.min_group_size = mean_group_size - group_size_tolerance


# [hphpph]
# [hp(hp)ph]

# def addTokenPair(return_string, token = 'p'):
# 	pair_type = random.choice(['split', 'left', 'right'])
# 	if pair_type = 'split':
# 		return token + return_string + token
# 	elif pair_type = 'left':

# 	else:

def order_tokens(tokens, fuselage = False, cluster_type = 'multiple'):
	return_string = ""
	if fuselage:
		return_string = "f"
	if cluster_type == 'single':
		if tokens["w"] > 0:
			return_string = "w"
		elif tokens['p'] == 0:
			return_string = "p"
		else:
			return_string = "(h)"
	else:
		if tokens["w'"] > 0:
			if tokens["w'"] > 2:
				#Cap w' at 4 for now
				if fuselage:
					if tokens['w']:
						while tokens['w'] > 0:
							return_string = 'w' + return_string
							tokens['w'] -= 1
							if  tokens['w'] > 0:
								return_string = return_string + 'w'
								tokens['w'] -= 1
				tokens["w'"] = 4
				while tokens["w'"] > 0:
					return_string = "w'" + return_string + "w'"
					tokens["w'"] -= 2
			else:
				if fuselage:
					if tokens['w'] > 0:
						while tokens['w'] > 0:
								return_string = 'w' + return_string
								tokens['w'] -= 1
								if  tokens['w'] > 0:
									return_string = return_string + 'w'
									tokens['w'] -= 1
					elif tokens['p'] == 1:
						return_string = "w'p" + return_string + "w'"
						tokens["w'"] -= 2
						tokens['p'] -= 1
					elif tokens['p'] > 1:
						return_string = "w'" + return_string + "w'"
						tokens["w'"] -= 2
						while tokens['p'] > 1:
							return_string = 'p' + return_string + 'p'
							tokens['p'] -= 2
					elif tokens['h'] > 1 :
						return_string = "w'" + return_string + "w'"
						tokens["w'"] -= 2
						while tokens['h'] > 1:
							return_string = 'h' + return_string + 'h'
							tokens['h'] -= 2
				else:
					if tokens['w'] > 0:
						return_string = "w'w" + return_string + "w'"
						tokens['w'] -= 1
						tokens["w'"] -= 2
					elif tokens['p'] > 1:
						return_string = "w'" + return_string + "w'"
						tokens["w'"] -= 2
						while tokens['p'] > 1:
							return_string = 'p' + return_string + 'p'
							tokens['p'] -= 2
					elif tokens['h'] > 1 :
						return_string = "w'" + return_string + "w'"
						while tokens['h'] > 1:
							return_string = 'h' + return_string + 'h'
							tokens['h'] -= 2
					else:
						return_string = "w'" + return_string + "w'"
						tokens["w'"] -= 2

		elif tokens['w'] > 0:
			if tokens['w'] > 3:
				tokens['w'] = 3
			while tokens['w']:
				return_string = 'w' + return_string
				tokens['w'] -= 1
				if tokens['w']:
					return_string = return_string + 'w'
					tokens['w'] -= 1
		else:
			schema = random.choice(['stacked','alternating','grouped'])
			if tokens['p'] % 2 == 1 and tokens['h'] % 2 == 0:
				return_string = place_schema(tokens, s_type = schema, centerpiece = 'p')
			elif tokens['h'] % 2 == 1 and tokens['p'] % 2 == 0:
				return_string = place_schema(tokens, s_type = schema, centerpiece = 'h')
			else:
				return_string = place_schema(tokens, s_type = schema)
	if return_string == "" : 
		print(tokens)
	return '[' + return_string + ']'



def selectTokens(valid_tokens, number, probs=None):
    if not probs:
        probs = [1 for x in list(valid_tokens.keys())]
    for x in range(number):
        valid_tokens[random.choices(list(valid_tokens.keys()), weights=probs, k=1)[0]] += 1
    valid_tokens['w'] = (valid_tokens['w']//2) * 2
    valid_tokens['w\''] = (valid_tokens['w\''] // 2) * 2



def run():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('designs', metavar='N', type=int,
                        help='number of designs to be generated')
    parser.add_argument('--clusters', dest="clusters", type=int, default=3,
                        help='number of clusters in a given design')
    parser.add_argument('--cluster_size_range', dest="cluster_range", type=int, nargs=2, default=[4,6],
                        help='range of number of parts in a cluster')
    parser.add_argument('--token_distribution', dest="token_dist", type=float, nargs=4, default=[.7, .2, .2, .6],
                        help='''Weights for selecting vertical propellers, horizontal propellers, 
                        wings and parallel wings respectively''')
    parser.add_argument('--output_file', dest="output", type=str, default="output.csv",
                        help="file path for strings to be output")
    args = parser.parse_args()

    file = open(args.output, 'w')

    for i in range(args.designs):
        tokens = {'p': 0, 'h': 0, 'w': 0, 'w\'': 0}
        selectTokens(tokens, random.randint(args.cluster_range[0],args.cluster_range[1]), args.token_dist)
        # schema = place_schema(tokens, s_type = "stacked")
        # print(schema)
        tokens["w'"] += 2 if tokens["w'"] == 0 else 0
        design = order_tokens(tokens, fuselage=True)
        j = 1
        while j < args.clusters:
            selectTokens(tokens, random.randint(args.cluster_range[0], args.cluster_range[1]), args.token_dist)
            design = order_tokens(tokens) + design
            j += 1
            if j < args.clusters:

                selectTokens(tokens, random.randint(args.cluster_range[0], args.cluster_range[1]),
                            args.token_dist)
                cluster = order_tokens(tokens)
                design = design + cluster
                j += 1

        print(design)
        file.write(design + "\n")





if __name__ == '__main__':
    run()
