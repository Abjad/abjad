from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class Ratio(ImmutableAbjadObject, tuple):
    '''.. versionadded:: 2.10

    Ratio of two or more nonzero integers::

        >>> from abjad.tools import mathtools

    ::

        >>> ratio = mathtools.Ratio(1, 2, 1)
        >>> ratio
        Ratio(1, 2, 1)

    Use a tuple to return ratio integers.

        >>> tuple(ratio)
        (1, 2, 1)
    
    Ratios are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(klass, *args):
        assert 2 <= len(args), repr(args)
        assert all([x != 0 for x in args]), repr(args) 
        self = tuple.__new__(klass, args)
        return self

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return tuple(self)
