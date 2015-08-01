# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class Talea(AbjadValueObject):
    '''Talea.

    ..  container:: example

        ::

            >>> talea = rhythmmakertools.Talea(
            ...    counts=(2, 1, 3, 2, 4, 1, 1),
            ...    denominator=16,
            ...    )

    ..  container:: example

        ::

            >>> talea[2]
            NonreducedFraction(3, 16)

    ..  container:: example

        ::

            >>> for nonreduced_fraction in talea[3:9]:
            ...     nonreduced_fraction
            ...
            NonreducedFraction(2, 16)
            NonreducedFraction(4, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(2, 16)
            NonreducedFraction(1, 16)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_counts',
        '_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=(1,),
        denominator=16,
        ):
        counts = self._to_tuple(counts)
        assert isinstance(counts, tuple)
        assert all(isinstance(x, int) for x in counts)
        self._counts = counts
        assert mathtools.is_nonnegative_integer_power_of_two(denominator)
        self._denominator = denominator

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a talea with `counts` and `denominator`
        equal to those of this talea. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __getitem__(self, item):
        r'''Gets non-reduced fraction at `item` cyclically.

        Returns non-reduced fraction or non-reduced fractions.
        '''
        counts = datastructuretools.CyclicTuple(self.counts)
        if isinstance(item, int):
            count = counts[item]
            return mathtools.NonreducedFraction(count, self.denominator)
        elif isinstance(item, slice):
            counts = counts[item]
            result = [mathtools.NonreducedFraction(count, self.denominator)
                for count in counts]
            return result
        raise ValueError(item)

    def __hash__(self):
        r'''Hashes talea.

        Returns integer.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __iter__(self):
        r'''Iterates talea.

        ..  container:: example

            ::

                >>> talea = rhythmmakertools.Talea(
                ...    counts=(2, 1, 3, 2, 4, 1, 1),
                ...    denominator=16,
                ...    )
                >>> for duration in talea:
                ...     duration
                ...
                Duration(1, 8)
                Duration(1, 16)
                Duration(3, 16)
                Duration(1, 8)
                Duration(1, 4)
                Duration(1, 16)
                Duration(1, 16)

        Yields durations.
        '''
        for count in self.counts:
            duration = durationtools.Duration(count, self.denominator)
            yield duration

    def __len__(self):
        r'''Gets length of talea.

        Returns integer.
        '''
        return len(self.counts)

    ### PRIVATE METHODS ###

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of talea.

        Returns tuple.
        '''
        return self._counts

    @property
    def denominator(self):
        r'''Gets denominator of talea.

        Returns nonnegative integer power of two.
        '''
        return self._denominator