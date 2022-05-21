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

import argparse
from grammar import StringGrammar
from grid import SnapGrid


def run():
    parser = argparse.ArgumentParser(description="parameters for string generation of designs")

    #  grammar args
    parser.add_argument('--n', type=int, default=50, help="# samples to generate")
    parser.add_argument('--len', type=int, default=10, help="max string length of design")
    parser.add_argument('--br', type=int, default=2, help="max # cylinders to connect together")
    parser.add_argument('--ho', action='store_true', help="use horizontal propellers")
    parser.add_argument('--sym', action='store_true', help="make symmetric designs")
    parser.add_argument('--pow', action='store_true', help="mount propellers on wings")
    parser.add_argument('--mut', action='store_true', help="mutate generated designs")

    #  management
    parser.add_argument('--sav', action='store_true', help="save the strings/mutants to pkl")

    args = parser.parse_args()

    print(args)

    sg = StringGrammar(args.n,
                       args.len,
                       args.br,  # default 2
                       args.ho,  # default False
                       args.sym,  # default False
                       args.pow,  # default False
                       args.mut,  # default True
                       args.sav)  # default False

    # create design strings
    sg.gen()

    if args.mut:
        sg.mut()

    #assert sg.generated is not None and sg.mutants is not None
    print("generated and mutated design strings")
    print(sg.get_generated_designs()[:10])
    print(sg.get_mutated_designs()[:10])
    # square_grid = SnapGrid(geo='square')
    # tri_grid = SnapGrid(geo='tri')
    # hex_grid = SnapGrid(geo='hex')



if __name__ == "__main__":
    run()