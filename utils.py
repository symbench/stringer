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


def save_design_strings(orderings, fpath):
    with open(fpath, 'a') as of:
        of.write("\n".join(orderings))

def read_design_strings(fpath):
    with open(fpath) as infile:
        return list(infile.readlines())


def remove_blanks(fpath):
    with open(fpath, 'r+') as file:
        for line in file:
            if not line.isspace():
                file.write(line)


def remove_duplicates(fpath):
    ords = read_design_strings(fpath)
    ords_dedup = list(set(sorted(ords)))
    save_design_strings(ords_dedup, fpath)
    remove_blanks(fpath)


p = "/Users/michael/darpa/stringer/data/20/designs"
print(read_design_strings(p))