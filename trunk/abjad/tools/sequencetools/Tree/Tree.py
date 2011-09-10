class Tree(list):
    r'''.. versionadded:: 2.4

    Arbitrarily nested lists extended with public `parent` attribute::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [0, 1, [2, 3, [4]], 5]
        abjad> tree = sequencetools.Tree(sequence)

    ::

        abjad> tree
        [0, 1, [2, 3, [4]], 5]

    ::

        abjad> tree[2][2]
        [4]

    ::

        abjad> tree[2][2].parent
        [2, 3, [4]]

    ::
    
        abjad> tree.parent is None
        True

    Trees overload list initializer.

    Trees otherwise inherit from list exactly.
    '''

    def __init__(self, expr):
        self.parent = None
        self.payload = None
        try:
            for element in expr:
                node = type(self)(element)
                node.parent = self
                self.append(node)
        except TypeError:
            self.payload = expr

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def __str__(self):
        if self.payload is None:
            return '[%s]' % ', '.join([str(x) for x in self])
        else:
            return repr(self.payload)

    ### PUBLIC ATTRIBUTES ###

    @property
    def depth(self):
        return len(self.parentage)

    @property
    def parentage(self):
        result = []
        cur = self.parent
        while cur is not None:
            result.append(cur)
            cur = cur.parent
        return result

    ### PUBLIC METHODS ###

    def iterate_at_depth(self, depth):
        for x in self.iterate_depth_first():
            if x.depth == depth:
                yield x

    def iterate_depth_first(self):
        yield self
        for x in self:
            for y in x.iterate_depth_first():
                yield y

    def iterate_leaves(self):
        for x in self.iterate_depth_first():
            if not len(x):
                yield x
            
    def iterate_payload(self):
        for x in self:
            if x.payload is not None:
                yield x.payload
            else:
                for y in x:
                    if y.payload is not None:
                        yield y.payload
                    for z in y.iterate_payload():
                        yield z
