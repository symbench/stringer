# Copyright (C) 2022, Michael Sandborn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


import random
from tqdm import tqdm
import os



"""
Todo
- make horizontal props prime
- change weights of symbols
- symmetric on one or more axes
-

generated string with structure --> convert that to graph (undirected, weighted edges or attributes)
    --> add directions / top sort (bookkeeping/readability/sanity check)

fuselage (passengers), wings (batteries), cylinders, propellers (motors) -- design/connection sequence
"""
class StringGrammar:

    config_dict = {'symbols': {'v': 0.5,  # vertical propeller
                               'f': 0.1,  # fuselage
                               'r': 0.2,  # rail, multiple cylinders connected in row to hold props
                               'w': 0.2},  # single wing
                    # todo probability of grouping [ and (
                    # todo assert even numbers in group ( and balanced wings in [
                   'num_samples': 100,  # number of strings to generate
                   'max_len': 10,  # max length of string allowed
                   'horizontal_props': False,  # use horizontal props in horizontal position
                   'min_vertical': 1,  # the minimum number of vertical propellers that must be present on a design
                   'min_horizontal': 0,  # " .. horizontal .. "
                   'min_wings': 2,  # minimum number of wings
                   'min_fuselage': 1,  # " .. fuselage .. "
                   'symmetric': False,  # produce symmetric designs
                   'mutate': False,  # produce mutations of generated designs
                   'mutations': {'flip_orient': 0.15,  # reverse the non-base elements of the string
                                 'push_prop': 0.3,  # add a propeller
                                 'pop_prop': 0.15,  # remove a propeller
                                 'pop_wing': 0.15,  # remove a wing
                                 'push_wing': 0.25},  # add a wing
                   #  todo add mutation for regrouping
                   'interpret_direction': 'fb',  # bf -- front to back or back to front, which way to read the string
                   'props_on_wings': False,  # mount propellers onto the wings
                   'branch_factor': 2,  # increase frequency of cylinders
                   'connection_angles': [30, 45, 60, 90, 180]  # degrees to connect components
                   #  todo allowable connections: check model to determine valid
                   }

    """
    Connections (check remote machine with e.g. trowel and rake to check on these: 
    
    cylinder_flip
    orient
    (wing-->battery)
    naca2port
    (fuselage-->seats)
    (prop-->motor)
    """

    def __init__(self, num_samples, max_len, branch_factor=2, horizontal_props=False, symmetric=False,
                 props_on_wings=False, mutate=False, save=False):

        #  change defaults from command line args
        if self.config_dict['num_samples'] != num_samples:
            self.config_dict['num_samples'] = num_samples

        if self.config_dict['max_len'] != max_len:
            self.config_dict['max_len'] = max_len

        if branch_factor != 2:
            assert branch_factor in range(1, 5)
            self.config_dict['branch_factor'] = branch_factor
            cf = self.config_dict['frequency']['r']

            #  small increase to connector frequency for higher branch factor (semi-arbitrary)
            self.config_dict['frequency']['r'] = cf * (branch_factor ** .1)

        if horizontal_props:
            self.config_dict['horizontal_props'] = True
            #  redistribute symbol weights
            self.config_dict['symbols'].update({'h': 0.15})
            self.config_dict['symbols']['v'] = 0.35

        if symmetric:  # todo account for this in generation routine
            self.config_dict['symmetric'] = True
        if props_on_wings:  # todo account for this in generation routine
            self.config_dict['props_on_wings'] = True
        if mutate:
            self.config_dict['mutate'] = True

        # save generated
        self.save = save
        self.save_dir = os.path.join(os.getcwd(), 'generated')

        # track past designs stored as lists of generators
        self.design_strings = {}
        #  map between original design strings and labeled design strings
        self.labeled_designs = {'generated': {}, 'mutants': {}}


    def _frequency_total(self):
        print(f"frequency total: {sum(self.config_dict['frequency'].values())}")

    def _is_valid(self, generated_string):
        lgs = list(generated_string)
        #lgs.count('')
        return 'w' in lgs and lgs.count('w') >= 2 and 'v' in lgs and\
               'f' in lgs and len(generated_string) <= self.config_dict['max_len']

    def _generate(self):

        freq = list(self.config_dict['symbols'].values())
        symbols = list(self.config_dict['symbols'].keys())
        max_len = self.config_dict['max_len']
        count = 0

        # track already created designs
        generated = []

        base = "wfwv"  # minimum viable vehicle -ø-
        n = self.config_dict['num_samples']
        pbar = tqdm(total=n)
        while count < n:
            gen_str = "".join(random.choices(list(self.config_dict['symbols'].keys()),
                                             weights=list(self.config_dict['symbols'].values()),
                                             k=random.choice(range(1, max_len - len(base) + 1))))
            if self._is_valid(base + gen_str):
                count += 1
                generated.append(base + gen_str)
                pbar.update(1)
                #yield base + gen_str
        pbar.close()
        return generated

    def gen(self):
        #  add generated designs to a history
        self.design_strings['generated'] = self._generate()

    def get_generated_designs(self):
        return list(self.design_strings['generated'])

    def get_mutated_designs(self):
        return list(self.design_strings['mutants'])

    def _mutate(self):

        use_horizontal = self.config_dict['horizontal_props']

        #  todo add valid mutation check
        def pick_prop():
            return random.choice(['h', 'v'])

        def pick_idx(lst):
            return random.randint(0, len(lst))


        #  todo move this with singular choice inside the for loop for each non-mutated design string
        # muts = random.choices(list(self.config_dict['mutations'].keys()),
        #                       weights=list(self.config_dict['mutations'].values()),
        #                       k=self.config_dict['num_samples'])

        def horizontal_present(cl):
            return 'h' in cl if use_horizontal else False

        def is_valid_mutation(ds, mut):
            char_list = list(ds)
            if mut == "pop_prop":
                if char_list.count('v') < 2:
                    return False
                return True
            elif mut == "pop_wing":
                return not char_list.count('w') < 3
            return True

        mutated_designs = []

        for idx in range(len(self.design_strings['generated'])):

            design_to_mutate = self.design_strings['generated'][idx]

            #  pick a valid mutation
            mutation = random.choices(list(self.config_dict['mutations'].keys()),
                                      weights=list(self.config_dict['mutations'].values()))[0]
            while not is_valid_mutation(design_to_mutate, mutation):
                mutation = random.choices(list(self.config_dict['mutations'].keys()),
                                          weights=list(self.config_dict['mutations'].values()))[0]

            char_list = list(design_to_mutate)

            if mutation == "pop_prop":  # remove a v or h prop
                assert char_list.count('v') > 1
                if use_horizontal and horizontal_present(char_list):
                    char_list.remove(pick_prop())
                else:
                    char_list.remove('v')

            elif mutation == "push_prop":  # add a v or h prop in random loc
                if use_horizontal:
                    char_list.insert(pick_idx(char_list), pick_prop())
                else:
                    char_list.insert(pick_idx(char_list), 'v')

            elif mutation == "pop_wing":  # remove a single wing
                char_list.remove('w')

            elif mutation == "push_wing":  # add a single wing
                char_list.insert(pick_idx(char_list), 'w')

            elif mutation == "flip_orient":
                #  todo consider changing interpretation direction
                char_list = char_list[:4] + char_list[3:][::-1]

            res = "".join(char_list)
            print(f"attempting mutation: [{mutation}] on design string: {design_to_mutate} --> {res}")
            mutated_designs.append(res)
        return mutated_designs

    def mut(self):
        self.design_strings['mutants'] = self._mutate()

    #  assign a score to the vehicle based on compactness/ space efficiency / height
    def score(self):
        pass

    # construct representative strings from the PI meeting
    # submitted designs, and visualize these as baselines
    def _view_seeds(self):
        """
        shovel -
        sputnik -
        bugger - [(pppppppppppp)(pppppppppppp)][wfw][(pppppppppppp)(pppppppppppp)]
        vudoo -
        vanderfool -
        joyride - [(hh)(hh)][w'bw's]s[ww]
        vunderkind -
        """
        pass

    #  for each generated string apply labels to them so that
    #  the same components have an integer label applied to them
    #  e.g. "wfwvhh" --> "w1f1w2v1h1h2"
    def label_generated(self):
        #  todo add labels to generated components
        for g in self.design_strings:
            char_list = list(g)


    #  from the labeled designs strings produce a connection graph
    #  that is undirected
    def create_graph_adjacency(self):
        pass

    #  augmen the existing adjacency matrix with connection angles
    def add_connection_angles(self):
        pass

    #  filter generated designs by component count, length, etc
    def filter(self):
        pass

    # todo write the storage object to json
    def _save(self):
        import time
        fname = time.strftime("%Y%m%d-%H%M%S") + ".pkl"
        fpath = os.path.join(self.save_dir, fname)