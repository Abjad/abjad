# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class NonreducedRatio(AbjadObject, tuple):
    '''Nonreduced ratio of one or more nonzero integers.

    Initialize from one or more nonzero integers:

    ::

        >>> mathtools.NonreducedRatio(2, 4, 2)
        NonreducedRatio(2, 4, 2)

    Or initialize from a tuple or list:

    ::

        >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
        >>> ratio
        NonreducedRatio(2, 4, 2)

    Use a tuple to return ratio integers.

        >>> tuple(ratio)
        (2, 4, 2)

    Nonreduced ratios are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(cls, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        elif len(args) == 0:
            args = (1, 1)
        assert args, repr(args)
        assert all(x != 0 for x in args), repr(args)
        self = tuple.__new__(cls, args)
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        expr = type(self)(expr)
        return tuple(self) == tuple(expr)

    def __format__(self, format_specification=''):
        r'''Formats duration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=tuple(self),
            )
