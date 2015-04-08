# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SplitByRoundedRatiosDivisionCallback(AbjadValueObject):
    r'''Rounded ratio division maker.

    ..  container:: example

        **Example 1.** Makes divisions with ``2:1`` ratios:

        ::

            >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
            ...     ratios=[mathtools.Ratio(2, 1)],
            ...     )
            >>> lists = maker([(7, 4), (6, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(5, 4), Division(2, 4)]
            [Division(4, 4), Division(2, 4)]

    ..  container:: example

        **Example 2.** Makes divisions with alternating ``2:1`` and ``1:1:1``
        ratios:

        ::

            >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
            ...     ratios=[mathtools.Ratio(2, 1), mathtools.Ratio(1, 1, 1)],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(5, 4), Division(2, 4)]
            [Division(2, 4), Division(2, 4), Division(2, 4)]
            [Division(3, 4), Division(2, 4)]
            [Division(1, 4), Division(2, 4), Division(1, 4)]

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output. Output structured one output list per input
    division.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_ratios',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ratios=None,
        ):
        if ratios is not None:
            ratios = ratios or ()
            ratios = [mathtools.Ratio(_) for _ in ratios]
            ratios = tuple(ratios)
        self._ratios = ratios

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls rounded ratio division maker on `division`.

        ..  container:: example

            **Example 1.** Calls maker on nonempty input:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(1, 1)],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(4, 4), Division(3, 4)]
                [Division(3, 4), Division(3, 4)]

            Returns list of division lists.

        ..  container:: example

            **Example 2.** Calls maker on empty input:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(1, 1)],
                ...     )
                >>> maker([])
                []

            Returns empty list.

        Returns possibly empty list of division lists.
        '''
        input_divisions = divisions or []
        if not input_divisions:
            return []
        output_division_lists = []
        ratios = self._get_ratios()
        for i, input_division in enumerate(input_divisions):
            input_division = durationtools.Division(input_division)
            ratio = ratios[i]
            numerators = mathtools.partition_integer_by_ratio(
                input_division.numerator,
                ratio,
                )
            output_division_list = [
                durationtools.Division(
                    numerator,
                    input_division.denominator,
                    )
                for numerator in numerators
                ]
            output_division_lists.append(output_division_list)
        return output_division_lists

    ### PRIVATE METHODS ###

    def _get_ratios(self):
        if self.ratios:
            ratios = self.ratios
        else:
            ratios = (mathtools.Ratio(1),)
        ratios = datastructuretools.CyclicTuple(ratios)
        return ratios

    ### PUBLIC PROPERTIES ###

    @property
    def ratios(self):
        r'''Gets ratios of rounded ratio division maker.

        ..  container:: example

            **Example 1.** Gets trivial ratio of ``1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(1)],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(7, 4)]
                [Division(6, 4)]

            This is default behavior when `ratios` is set to none.

        ..  container:: example

            **Example 2.** Gets ratios equal to ``1:1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(1, 1)],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(4, 4), Division(3, 4)]
                [Division(3, 4), Division(3, 4)]

        ..  container:: example

            **Example 3.** Gets ratios equal to ``2:1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(2, 1)],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(5, 4), Division(2, 4)]
                [Division(4, 4), Division(2, 4)]

        ..  container:: example

            **Example 4.** Gets ratios equal to ``1:1:1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(1, 1, 1)],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(2, 4), Division(3, 4), Division(2, 4)]
                [Division(2, 4), Division(2, 4), Division(2, 4)]

        ..  container:: example

            **Example 5.** Gets ratios equal to ``2:1`` and ``1:1:1``
            alternately:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio(2, 1), mathtools.Ratio(1, 1, 1)],
                ...     )
                >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(5, 4), Division(2, 4)]
                [Division(2, 4), Division(2, 4), Division(2, 4)]
                [Division(3, 4), Division(2, 4)]
                [Division(1, 4), Division(2, 4), Division(1, 4)]

        Set to ratios or none.
        '''
        return self._ratios