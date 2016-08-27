# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class Talea(AbjadValueObject):
    '''Talea.

    ..  container:: example

        **Example.**

        ::

            >>> talea = rhythmmakertools.Talea(
            ...    counts=(2, 1, 3, 2, 4, 1, 1),
            ...    denominator=16,
            ...    )

    The medieval plural of 'talea' is 'talee'. Abjad documentation
    uses 'taleas' instead.
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
        counts = tuple(counts)
        assert all(isinstance(x, int) for x in counts)
        self._counts = counts
        if not mathtools.is_nonnegative_integer_power_of_two(denominator):
            message = 'denominator must be integer power of 2: {!r}.'
            message = message.format(denominator)
            raise Exception(message)
        self._denominator = denominator

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        r'''Gets nonreduced fraction at `item` cyclically.

        ..  container:: example

            **Example 1.** Gets item at index:

            ::

                >>> talea = rhythmmakertools.Talea(
                ...    counts=(2, 1, 3, 2, 4, 1, 1),
                ...    denominator=16,
                ...    )

            ::

                >>> talea[2]
                NonreducedFraction(3, 16)

        ..  container:: example

            **Example 2.** Gets items in slice:

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

        Returns nonreduced fraction or nonreduced fractions.
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

    def __iter__(self):
        r'''Iterates talea.

        ..  container:: example

            **Example.**

            ::

                >>> talea = rhythmmakertools.Talea(
                ...    counts=(2, 1, 3, 2, 4, 1, 1),
                ...    denominator=16,
                ...    )

            ::

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
        r'''Gets length.

        ..  container:: example

            **Example.**

            ::

                >>> talea = rhythmmakertools.Talea(
                ...    counts=(2, 1, 3, 2, 4, 1, 1),
                ...    denominator=16,
                ...    )

            ::

                >>> len(talea)
                7

        Defined equal to length of counts.

        Returns nonnegative integer.
        '''
        return len(self.counts)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts.

        ..  container:: example

            **Example.**

            ::

                >>> talea = rhythmmakertools.Talea(
                ...    counts=(2, 1, 3, 2, 4, 1, 1),
                ...    denominator=16,
                ...    )

            ::

                >>> talea.counts
                (2, 1, 3, 2, 4, 1, 1)

        Set to integers.

        Defaults to `(1,)`.

        Returns tuple.
        '''
        return self._counts

    @property
    def denominator(self):
        r'''Gets denominator.

        ..  container:: example

            **Example.**

            ::

                >>> talea = rhythmmakertools.Talea(
                ...    counts=(2, 1, 3, 2, 4, 1, 1),
                ...    denominator=16,
                ...    )

            ::

                >>> talea.denominator
                16

        Set to nonnegative integer power of two.

        Defaults to 16.

        Returns nonnegative integer power of two.
        '''
        return self._denominator
