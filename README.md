Stringer is meant to inspire human designers with aircraft vehicle layouts encoded as strings

The core intuition is that the collective combinatorial space of locations, connections, orientations, and
arrangements explodes with more design elements, so we aim to compactly represent these layouts and learn from simulation
results.

Stringer produces strings that are specified from a grammar which comes from a user-specified configuration dictionary to
specify layout properties. These strings are then interpreted into a graph by resolving connections between components and
their spatial relationships.  The goal from here is to assign an integer score to these designs based on geometric properties such as the
compactness of the design, the number of total components, etc. and then mutate them in a pointwise fashion later on.

Later, a human design can introduce optimal components to "fill in the blanks" provided by
the interpreted design string. In other words, the designer inputs a configuration and generates strings. These strings are
then interpreted based on the provided configuration and each string represents a unique design layout under the given 
configuration dictionary. Later, designs should be filtered based on feasibility. For example, a design with fewer propellers
should have larger propellers and vice versa for more/smaller propellers. Additionally, all vehicles are required to
adhere to the base model which contains a single fuselage and two wings.

The goal of this project is not to produce fully functional vehicles, select components, or assign component parameters.
Rather it is meant to provide design inspiration to a downstream routine or human that selects concrete component instances
in the locations encoded by the design strings/graphs and then optimize these parameters in a surrogate simulation for
example.

With this construction, we remove the need for exploration over a complicated multi-domain space such as
the electrical/aerospace/physics domains. However, data from these domains that come from simulating fully-specified
designs may be useful in informing what makes a productive or high quality design. This information can be incorporated
into e.g. an evolutionary routine that is capable of selecting and generating new designs and manipulating existing ones
based on these qualities. As an initial step in this direction, we provide a few basic mutations to design strings.

### Usage
`grammar.py` contains the `StringGrammar` class which contains the code to specify and generate/manipulate/save
design strings. A user specifies command line options in `cli.py` to modify the `config_dict` of a `StringGrammar`
object at initialization. The `gen()` function of `StringGrammar` produces design strings based on the modified
`config_dict` from user input. Generated designs are stored in `StringGrammar.design_strings['generated']`.
The `mut()` function will randomly select a point mutation for each generated string and then, after ensuring it is valid for
the given design string, apply the mutation. These strings are stored in `StringGrammar.design_strings['mutants']`.

### TODO - in no particular order
- [x] create a string grammar to produce strings satisfying constraints in the user-specified `config_dict`
- [ ] create a graph adjacency matrix and accompanying edge labels (connection angles) for design strings (wip)
- [x] incorporate layout grouping with ( ) and [ ] from Carlos's approach
- [x] produce handcrafted design strings from the 7 seed designs from hackathon 2 as a sanity check
- [x] introduce basic mutations to the strings to modify component layout/ orientation
- [ ] add granular functionality to mutate one or more selected design strings rather than all previously generated ones