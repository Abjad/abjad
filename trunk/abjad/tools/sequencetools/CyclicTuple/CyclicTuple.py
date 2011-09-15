class CyclicTuple(tuple):
    '''.. versionadded:: 2.0

    Abjad model of cyclic tuple::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> cyclic_tuple = sequencetools.CyclicTuple('abcd')

    ::

        abjad> cyclic_tuple
        CyclicTuple([a, b, c, d])

    ::

        abjad> for x in range(8):
        ...     print x, cyclic_tuple[x]
        ...
        0 a
        1 b
        2 c
        3 d
        4 a
        5 b
        6 c
        7 d

    Cyclic tuples overload the item-getting method of built-in tuples.

    Cyclic tuples return a value for any integer index.

    Cyclic tuples otherwise behave exactly like built-in tuples.
    '''

    ### OVERLOADS ###

    def __getitem__(self, expr):
        return tuple.__getitem__(self, expr % len(self))

    def __getslice__(self, start_index, stop_index):
        result = []
        result = [self[n] for n in range(start_index, stop_index)]
        return tuple(result)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def __str__(self):
        return '[%s]' % ', '.join([str(x) for x in self])
