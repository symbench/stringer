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


def orderTokens(tokens, in_bracket=True, endcap=False, contains_fuselage = False, branching_coefficient=50):
    return_string = ''
    if contains_fuselage:
        endcap = True
        return_string = "f"
        tokens["w'"] = 2

    if tokens["h"] == 1:
        # One horizontal propeller
        if tokens["w'"] > 0:
            # There are parallel wings
            if tokens['p'] % 2 == 1:
                # If there are an odd number of vertical propellers, one must be in the center
                if endcap:
                    # If there is only 1 horizontal propeller AND we are at the end
                    # of the generation, h could either cap the principal axis or
                    # be on a branch.
                    if random.randint(0, 100) < branching_coefficient:
                        return_string = return_string + "(hp)"
                    else:
                        return_string = return_string + "hp"
                    for x in range(tokens["w'"] // 2):
                        return_string = "w'" + return_string + "w'"
                    # [hphwwhph] (h)p(hh)p(h)
                    for x in range(tokens["p"] // 2):
                        return_string = "p" + return_string + "p"
                # [(pp)w'hpw'(pp)] [ppw'hpw'pp]
                else:
                    # If this is not at the endcap, must have a separate connector
                    return_string = return_string + "(hp)"
                    for x in range(tokens["w'"] // 2):
                        return_string = "w'" + return_string + "w'"
                    for x in range(tokens["p"] // 2):
                        return_string = "p" + return_string + "p"
            else:
                # number of vertical propellers is even
                if endcap:
                    # If there is only 1 horizontal propeller AND we are at the end
                    # of the generation, h could either cap the principal axis or
                    # be on a branch.
                    if random.randint(0, 100) < branching_coefficient:
                        return_string = return_string + "(h)"
                    else:
                        return_string = return_string + "h"
                    for x in range(tokens["w'"] // 2):
                        return_string = "w'" + return_string + "w'"
                    for x in range(tokens["p"] // 2):
                        return_string = "p" + return_string + "p"
                else:
                    # If this is not at the endcap, must have a separate connector
                    return_string = return_string + "(hp)"
                    for x in range(tokens["w'"] // 2):
                        return_string = "w'" + return_string + "w'"
                    for x in range(tokens["p"] // 2):
                        return_string = "p" + return_string + "p"
        else:
            # there are no parallel wings
            if tokens['w'] > 0:
                # there are non-parallel wings
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    if endcap:
                        # If there is only 1 horizontal propeller AND we are at the end
                        # of the generation, h could either cap the principal axis or
                        # be on a branch.
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(hp)"
                        else:
                            return_string = return_string + "hp"
                        for x in range(tokens["w"] // 2):
                            return_string = "w" + return_string + "w"
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                    else:
                        # If this is not at the endcap, must have a separate connector
                        return_string = return_string + "(hp)"
                        for x in range(tokens["w"] // 2):
                            return_string = "w" + return_string + "w"
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                else:
                    # number of vertical propellers is even
                    if endcap:
                        # If there is only 1 horizontal propeller AND we are at the end
                        # of the generation, h could either cap the principal axis or
                        # be on a branch.
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(h)"
                        else:
                            return_string = return_string + "h"
                        for x in range(tokens["w'"] // 2):
                            return_string = "w'" + return_string + "w'"
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                    else:
                        # If this is not at the endcap, must have a separate connector
                        return_string = return_string + "(h)"
                        for x in range(tokens["w'"] // 2):
                            return_string = "w'" + return_string + "w'"
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
            else:
                # no wings of any sort
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    if endcap:
                        # If there is only 1 horizontal propeller AND we are at the end
                        # of the generation, h could either cap the principal axis or
                        # be on a branch.
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(hp)"
                        else:
                            return_string = return_string + "hp"
                        if tokens['p'] > 1:
                            for x in range(tokens["p"] // 2):
                                return_string = "p" + return_string + "p"
                            return_string = "(" + return_string + ")"
                    else:
                        # If this is not at the endcap, must have a separate connector
                        return_string = return_string + "(hp)"
                        if tokens['p'] > 1:
                            for x in range(tokens["p"] // 2):
                                return_string = "p" + return_string + "p"
                            return_string = "(" + return_string + ")"
                else:
                    # number of vertical propellers is even
                    if endcap:
                        # If there is only 1 horizontal propeller AND we are at the end
                        # of the generation, h could either cap the principal axis or
                        # be on a branch.
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(h)"
                        else:
                            return_string = return_string + "h"
                        if tokens['p'] > 1:
                            for x in range(tokens["p"] // 2):
                                return_string = "p" + return_string + "p"
                            return_string = "(" + return_string + ")"
                    else:
                        # If this is not at the endcap, must have a separate connector
                        return_string = return_string + "(h)"
                        if tokens['p'] > 1:
                            for x in range(tokens["p"] // 2):
                                return_string = "p" + return_string + "p"
                            return_string = "(" + return_string + ")"

    elif tokens["h"] == 0:
        # no horizontal propellers
        if tokens["w'"] > 0:
            # There are parallel wings
            if tokens['p'] % 2 == 1:
                # If there are an odd number of vertical propellers, one must be in the center
                if random.randint(0, 100) < branching_coefficient:
                    return_string = return_string + "(p)"
                else:
                    return_string = return_string + "p"
                for x in range(tokens["w'"] // 2):
                    return_string = "w'" + return_string + "w'"
                # [hphwwhph] (h)p(hh)p(h)
                for x in range(tokens["p"] // 2):
                    return_string = "p" + return_string + "p"

            else:
                # number of vertical propellers is even
                for x in range(tokens["w'"] // 2):
                    return_string = "w'" + return_string + "w'"
                for x in range(tokens["p"] // 2):
                    return_string = "p" + return_string + "p"
        else:
            # there are no parallel wings
            if tokens['w'] > 0:
                # there are non-parallel wings
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    if random.randint(0, 100) < branching_coefficient:
                        return_string = return_string + "(p)"
                    else:
                        return_string = return_string + "p"
                    for x in range(tokens["w"] // 2):
                        return_string = "w" + return_string + "w"
                    for x in range(tokens["p"] // 2):
                        return_string = "p" + return_string + "p"
                else:
                    # number of vertical propellers is even
                    for x in range(tokens["w'"] // 2):
                        return_string = "w'" + return_string + "w'"
                    for x in range(tokens["p"] // 2):
                        return_string = "p" + return_string + "p"

            else:
                # no wings of any sort
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    # TODO: consider removing this optional branching as it can lead to (pp(p)pp), may not make sense
                    if random.randint(0, 100) < branching_coefficient:
                        return_string = return_string + "(p)"
                    else:
                        return_string = return_string + "p"
                    if tokens['p'] > 1:
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                        return_string = "(" + return_string + ")"
                else:
                    # number of vertical propellers is even
                    if tokens['p'] > 1:
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                        return_string = "(" + return_string + ")"

    elif tokens["h"] % 2 == 0:
        # number of horizontal propellers is even
        if tokens["w'"] > 0:
            # There are parallel wings
            if tokens['p'] % 2 == 1:
                # If there are an odd number of vertical propellers, one must be in the center
                if random.randint(0, 100) < branching_coefficient:
                    return_string = return_string + "(p)"
                else:
                    return_string = return_string + "p"

            # number of vertical propellers is even
            for x in range(tokens["w'"] // 2):
                return_string = "w'" + return_string + "w'"
            for x in range(tokens["p"] // 2):
                return_string = "p" + return_string + "p"
            for x in range(tokens["h"] // 2):
                return_string = "h" + return_string + "h"
        else:
            # there are no parallel wings
            if tokens['w'] > 0:
                # there are non-parallel wings
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    if random.randint(0, 100) < branching_coefficient:
                        return_string = return_string + "(p)"
                    else:
                        return_string = return_string + "p"
                # number of vertical propellers is even
                for x in range(tokens["w'"] // 2):
                    return_string = "w'" + return_string + "w'"
                for x in range(tokens["p"] // 2):
                    return_string = "p" + return_string + "p"
                for x in range(tokens["h"] // 2):
                    return_string = "h" + return_string + "h"

            else:
                # no wings of any sort
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    if random.randint(0, 100) < branching_coefficient:
                        return_string = return_string + "(p)"
                    else:
                        return_string = return_string + "p"
                    if tokens['p'] > 1:
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                else:
                    # number of vertical propellers is even
                    if tokens['p'] > 1:
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                if tokens['h'] > 1:
                    for x in range(tokens["h"] // 2):
                        return_string = "h" + return_string + "h"
                    return_string = "(" + return_string + ")"
    elif tokens["h"] % 2 == 1:
        # number of horizontal propellers is odd
        if tokens["w'"] > 0:
            # There are parallel wings
            if tokens['p'] % 2 == 1:
                # If there are an odd number of vertical propellers, one must be in the center
                if random.randint(0, 100) < branching_coefficient:
                    return_string = return_string + "(hp)"
                else:
                    return_string = return_string + "hp"

            # number of vertical propellers is even
            for x in range(tokens["w'"] // 2):
                return_string = "w'" + return_string + "w'"
            for x in range(tokens["p"] // 2):
                return_string = "p" + return_string + "p"
            for x in range(tokens["h"] // 2):
                return_string = "h" + return_string + "h"
        else:
            # there are no parallel wings
            if tokens['w'] > 0:
                # there are non-parallel wings
                if tokens['p'] % 2 == 1:
                    # If there are an odd number of vertical propellers, one must be in the center
                    if endcap:
                        # If there are an odd number of vertical propellers, one must be in the center
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(hp)"
                        else:
                            return_string = return_string + "hp"
                    else:
                        # not at the endcap, requires a branch
                        return_string = return_string + "(hp)"
                # number of vertical propellers is even
                else:
                    if endcap:
                        # If there are an odd number of vertical propellers, one must be in the center
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(h)"
                        else:
                            return_string = return_string + "h"
                    else:
                        # not at the endcap, requires a branch
                        return_string = return_string + "(h)"
                for x in range(tokens["w'"] // 2):
                    return_string = "w'" + return_string + "w'"
                for x in range(tokens["p"] // 2):
                    return_string = "p" + return_string + "p"
                for x in range(tokens["h"] // 2):
                    return_string = "h" + return_string + "h"

            else:
                # no wings of any sort
                if tokens['p'] % 2 == 1:
                    if endcap:
                        # If there are an odd number of vertical propellers, one must be in the center
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(hp)"
                        else:
                            return_string = return_string + "hp"
                    else:
                        # not at the endcap, requires a branch
                        return_string = return_string + "(hp)"
                    if tokens['p'] > 1:
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                        return_string = "(" + return_string + ")"
                else:
                    # number of vertical propellers is even
                    if endcap:
                        # If there are an odd number of vertical propellers, one must be in the center
                        if random.randint(0, 100) < branching_coefficient:
                            return_string = return_string + "(h)"
                        else:
                            return_string = return_string + "h"
                    else:
                        # not at the endcap, requires a branch
                        return_string = return_string + "(h)"
                    if tokens['p'] > 1:
                        for x in range(tokens["p"] // 2):
                            return_string = "p" + return_string + "p"
                        return_string = "(" + return_string + ")"
                if tokens['h'] > 1:
                    for x in range(tokens["h"] // 2):
                        return_string = "h" + return_string + "h"
                    if not return_string[0] == "(":
                        return_string = "(" + return_string + ")"

    if in_bracket or tokens['w'] > 1 or tokens["w'"] > 1:
        # inside positional constraint
        return_string = "[" + return_string + "]"

    return return_string


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
        design = orderTokens(tokens, contains_fuselage=True)
        j = 1
        while j < args.clusters:
            selectTokens(tokens, random.randint(args.cluster_range[0], args.cluster_range[1]), args.token_dist)
            design = orderTokens(tokens) + design
            j += 1
            if j < args.clusters:

                selectTokens(tokens, random.randint(args.cluster_range[0], args.cluster_range[1]),
                            args.token_dist)
                cluster = orderTokens(tokens)
                design = design + cluster
                j += 1

        print(design)
        file.write(design + "\n")





if __name__ == '__main__':
    run()



