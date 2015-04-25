# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class NonreducedRatio(TypedTuple):
    '''Nonreduced ratio of one or more nonzero integers.

    ..  container:: example

        **Example 1.** Initializes from iterable of nonzero integers:

        ::

            >>> mathtools.NonreducedRatio((2, 4, 2))
            NonreducedRatio((2, 4, 2))

    ..  container:: example

        **Example 2.** Use a tuple to return ratio integers.

            >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
            >>> tuple(ratio)
            (2, 4, 2)

    Nonreduced ratios are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=(1, 1)):
        assert isinstance(items, collections.Sequence)
        superclass = super(NonreducedRatio, self)
        superclass.__init__(items=items)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a nonreduced ratio with numerator and
        denominator equal to those of this nonreduced ratio. Otherwise false.

        Returns boolean.
        '''
        expr = type(self)(expr)
        return tuple(self) == tuple(expr)

    def __format__(self, format_specification=''):
        r'''Formats duration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
                >>> print(format(ratio))
                mathtools.NonreducedRatio((2, 4, 2))

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        r'''Hashes non-reduced ratio.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NonreducedRatio, self).__hash__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        return int

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            tuple(self),
            )
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        r'''Gets multipliers implicit in ratio.

        ..  container:: example

            **Example 1.** Gets mutlipliers:

            ::

                >>> mathtools.NonreducedRatio((2, 4, 2)).multipliers
                (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        '''
        from abjad.tools import durationtools
        weight = sum(self) 
        multipliers = [durationtools.Multiplier((_, weight)) for _ in self]
        multipliers = tuple(multipliers)
        return multipliers
