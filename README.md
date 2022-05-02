Stringer (String designer or string exploration routine) is a lightweight routine to inspire human designers with vehicle layouts (aircraft in this case).

The core intuition is that the collective combinatorial space of locations, connections, orientations, and
arrangements explodes with more design elements (i.e. a more complicated vehicle).

Therefore we would like to introduce some structure that constrains this combinatorial space to a region that
is sufficiently smaller and easy to explore (assign importance or value to a design).

With this in mind, stringer produces strings that are specified from a grammar which comes from a
user provided configuration dictionary. This grammar can be used to generate strings of specified length and properties.
These strings are then expanded to resolve connections and lay components based on a bounding volume and a
layout interpretation direction. These strings can then be assigned a score based on purely geometric properties.

Later, a human design can introduce high-performing (e.g. pareto optimal) components to "fill in the blanks" provided by
the interpreted design string. In other words, the designer inputs a configuration and generates strings. These strings are
then interpreted based on the provided configuration and each string represents a unique design layout under the given 
configuration dictionary.

With this construction, we remove the need for exploration over a complicated multi-domain space such as
the electrical and aerospace domains. Instead, we 

### Grammar - specify allowable strings

This is how design constraints are specified and generated. A grammar takes a config
dictionary or uses the default and specifies symbols, connections, restrictions, and properties
that must be satisfied for generated strings

### Bounding volume - specify where objects can go in the layout

This is how the generated string/graph is laid out in space. The bounding volume dictates acceptable 
connection patterns for the vehicle and sequentially lays components according to the interpretation direction (e.g. 
starting from the left, right, or middle of the string - we want character location to matter in the generated
strings so there is value in learning from them and productive mutations later) which may be bottom up,
front to back, or left to right.

### TODO
- [ ] add expansion rules for interpreting strings
- [ ] add handling for layout of vehicle design
- [ ] implement draw or viz feature to see the design layout
- [ ] assign score to generated strings from purely geometric descriptors such as spanning area, total volume, and connection density
- [ ] introduce mutations to the strings to update the score to facilitate learning or improvement to string generation quality