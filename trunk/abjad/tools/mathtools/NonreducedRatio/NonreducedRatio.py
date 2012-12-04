from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class NonreducedRatio(ImmutableAbjadObject, tuple):
    '''.. versionadded:: 2.11

    Nonreduced ratio of one or more nonzero integers.

    Initialize from one or more nonzero integers::

        >>> mathtools.NonreducedRatio(2, 4, 2)
        NonreducedRatio(2, 4, 2)

    Or initialize from a tuple or list::

        >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
        >>> ratio
        NonreducedRatio(2, 4, 2)

    Use a tuple to return ratio integers.

        >>> tuple(ratio)
        (2, 4, 2)

    Nonreduced ratios are immutable.
    '''

    ### INITIALIZER ###

    def __new__(klass, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        assert args, repr(args)
        assert all([x != 0 for x in args]), repr(args) 
        self = tuple.__new__(klass, args)
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        other = type(self)(other)
        return tuple(self) == tuple(other)
        
    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return tuple(self)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            ImmutableAbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]
