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


import numpy as np
import pyvista as pv
import random
import os
import sys
from typing import List, Dict


"""
class to generate designs from string given a bounding geometry



"""
class SnapMesh:
    def __init__(self, geo='cube'):
        assert isinstance(geo, str)
        assert geo in ['cube', 'cylinder', 'sphere', 'pyramid']

        self.designs = {}

        values = np.linspace(0, 10, 1000).reshape((10, 10, 10))
        values.shape

        # Create the spatial reference
        grid = pv.UniformGrid()

        # Set the grid dimensions: shape + 1 because we want to inject our values on
        #   the CELL data
        grid.dimensions = np.array(values.shape) + 1

        # Edit the spatial reference
        grid.origin = (0, 0, 0)  # The bottom left corner of the data set
        grid.spacing = (4, 4, 4)  # These are the cell sizes along each axis

        # Add the data values to the cell data
        grid.cell_data["values"] = values.flatten(order="F")  # Flatten the array!

        # Now plot the grid!
        grid.plot(show_edges=True)

    # initialize the mesh object of specified geometry
    def _initialize(self):
        pass

    # display the expansion (from a design string) inside its bounding volume
    def _render(self, expansion):
        pass


"""
Class to manage and produce the strings given configuration and connection rules

"""
class StringGrammar:


    """
        Store the string generation rules in a config dictionary

        Keys:
            symbols (List[str]): the characters allowed in the vehicle string
            frequency (List[float]): the distribution to sample from when adding new characters


    """
    default_config = {'symbols': ['x', 'v', 'f', 'h', 'c'],  # component that are represented in design strings
                      #  x is a pair of wings, v is a vertical propellers, f is a fuselage, h is a horizontal propeller, c is a cylinder
                      'frequency': {'x': 0.2, 'v': 0.3, 'f': 0.1, 'h': 0.15, 'c': .25},  # how often each component appears
                      'max_len': 10,  # longest length of string allowed
                      'num_samples': 100,  # the number of strings to generate
                      'horizontal_props': False,  # use props in horizontal position
                      'min_vertical': 1,  # the minimum number of vertical propellers that must be present on a design
                      'min_horizontal': 0,  # " .. horizontal .. "
                      'min_wings': 2,  # minimum number of wings
                      'min_fuselage': 1,  # " .. fuselage .. "
                      'symmetric': True,  # produce symmetric designs
                      'mutations': ['flip_orient', 'push_prop', 'pop_prop', 'pop_wing', 'push_wing'],
                      'interpret_direction': 'fb',  # mo, bt --> front to back, middle out, bottom to top
                      'props_on_wings': False,  # mount propellers onto the wings
                      'branching_factor': 2,  # number of cylinders that can be connected together before connecting something else e.g. |-- = 2
                      }

    def __init__(self, config=default_config):
        self.config = config


    def is_valid(self, generated_string):
        lgs = list(generated_string)  # grab all characters
        lgs.count('')
        return 'x' in lgs and 'v' in lgs and 'f' in lgs and len(generated_string) <= self.config['max_len']

    def generate(self):
        if not self.config['horizontal_props']:
            self.config['symbols'].remove('h')
        symbols = self.config['symbols']

        count = 0
        while count < self.config['num_samples']:
            base = 'xvf'  # minimum viable vehicle
            gen_str = "".join(random.choices(symbols, weights=[self.config['frequency'][s] for s in symbols], k=random.choice(range(1, self.config['max_len'] - len(base) + 1))))
            if self.is_valid(base + gen_str):
                count += 1
                yield base + gen_str

    # from the original generated population, apply mutations in config
    def mutate(self):
        # indices = [i for i, x in enumerate(my_list) if x == "whatever"]
        pass

    def expand(self):
        pass

    # assign a score to the vehicle based on compactness/ space efficiency / height
    def score(self):
        pass


if __name__ == "__main__":
    sg = StringGrammar()
    generator = sg.generate()
    print(list(generator))