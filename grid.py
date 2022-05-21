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

import matplotlib.pyplot as plt


""" class representing where to contain the strings generated """
class SnapGrid:
    def __init__(self, geo='square', dim=2):

        # assert isinstance(designs, dict), f"invalid design structure! Expected dict, received {type(designs)}"
        # self.designs = designs
        #  store the intrepreted designs
        # self.designs_on_mesh = None

        assert dim == 2 or dim == 3, f"invalid dimension: {dim}"
        # todo 3d is not supported for now
        assert isinstance(geo, str)
        self.allowed_mesh = ['square', 'tri', 'hex']
        assert geo in self.allowed_mesh, f"invalid mesh structure: {geo}"
        #assert geo in ['cube', 'cylinder', 'sphere', 'pyramid']  # 3D, for later

        #  init geo shape and dimension
        self.geo = geo
        self.dim = dim
        self._create_mesh()

    # initialize the mesh object of specified geometry
    def _create_mesh(self):
        if self.geo == 'square':
            print(f"make {self.geo} mesh")
        elif self.geo == 'tri':
            print(f"make {self.geo} mesh")
        elif self.geo == 'hex':
            print(f"make {self.geo} mesh")

    # apply the initialized mesh to the specified designs
    def draw(self, design_strings, k=5):
        assert isinstance(design_strings, list)
        # todo meat and potatoes of this object, map the design strings to the grid
        pass

    # given a drawing of a mesh representing a design string, extract the graph of the design
    def extract_graph(self):
        pass