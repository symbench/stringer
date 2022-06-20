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
import random
from grammar_string_gen import selectTokens, orderTokens
from utils import *
import os


def run():
    parser = argparse.ArgumentParser(description="parameters for string generation of designs")

    #  grammar args
    parser.add_argument('--n', type=int, default=100, help="# samples to generate")
    parser.add_argument('--ntok', type=int, default=20)
    parser.add_argument('--outfile', type=str, default="./out.txt", help="path to store files")
#    parser.add_argument('--br', type=int, default=2, help="max # cylinders to connect together")
#    parser.add_argument('--br', type=int, default=2, help="max # cylinders to connect together")
#    parser.add_argument('--ho', action='store_true', help="use horizontal propellers")
#    parser.add_argument('--sym', action='store_true', help="make symmetric designs")
#    parser.add_argument('--pow', action='store_true', help="mount propellers on wings")
#    parser.add_argument('--mut', action='store_true', help="mutate generated designs")

    args = parser.parse_args()

    generate_count = args.n
    token_count = args.ntok
    token_selections = []
    for _ in range(generate_count):
        # random weights, fix these later
        probs = [random.randint(1, 9) / 10 for _ in range(4)]
        print(f"probs {probs}")
        tokens = {'p': 0, 'h': 0, 'w': 0, 'w\'': 0}
        selectTokens(tokens, token_count, probs)
        print(f"token counts: {tokens}")
        token_selections.append(tokens)

    orderings = []
    for s in token_selections:
        ordering = orderTokens(s)
        orderings.append(ordering)

    print(len(orderings))

    save_path = os.path.join(os.getcwd(), 'data', str(token_count), 'designs')
    save_design_strings(orderings, save_path)
    print("saved")

    remove_duplicates(save_path)

#    sg = StringGrammar(args.n,
#                       args.len,
#                       args.br,  # default 2
#                       args.ho,  # default False
#                       args.sym,  # default False
#                       args.pow,  # default False
#                       args.mut,  # default True
#                       args.sav)  # default False

    # create design strings
#    sg.gen()

 #   if args.mut:
 #       sg.mut()




if __name__ == "__main__":
    run()
