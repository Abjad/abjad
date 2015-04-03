# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BeatGroupDivisionMaker(AbjadValueObject):
    r'''Beat division-maker.

    ..  container:: example

        **Example 1.** Makes measures:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     depths=[0],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(7, 4)]
            [Division(6, 4)]
            [Division(5, 4)]
            [Division(4, 4)]

    ..  container:: example

        **Example 2.** Makes beat groups:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     depths=[1],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(3, 4), Division(2, 4), Division(2, 4)]
            [Division(3, 4), Division(3, 4)]
            [Division(3, 4), Division(2, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

    ..  container:: example

        **Example 3.** Makes beats:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     depths=[2],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

    ..  container:: example

        **Example 4.** Makes alternating measures and beat groups:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     depths=[0, 1],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(7, 4)]
            [Division(3, 4), Division(3, 4)]
            [Division(5, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output. Ouput is structured one output list per input
    division.

    Treats input as meters.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_decrease_durations_monotonically',
        '_depths',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_durations_monotonically=True,
        depths=None,
        ):
        if depths is not None:
            depths = depths or ()
            assert mathtools.all_are_nonnegative_integers(depths), repr(depths)
        self._depths = depths
        prototype = (type(None), type(True))
        assert isinstance(decrease_durations_monotonically, prototype)
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls beat division maker on `divisions`.

        ..  container:: example

            **Example 1.** Calls maker on nonempty input:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker(
                ...     depths=[1],
                ...     )
                >>> lists = maker([(7, 4), (6, 4), (5, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(3, 4), Division(2, 4), Division(2, 4)]
                [Division(3, 4), Division(3, 4)]
                [Division(3, 4), Division(2, 4)]

            Returns list of division lists.

        ..  container:: example

            **Example 2.** Calls maker on empty input:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker(
                ...     depths=[1],
                ...     )
                >>> lists = maker([])
                >>> lists
                []

            Returns empty list.

        Returns (possibly empty) list of division lists.
        '''
        input_divisions = divisions or []
        if not input_divisions:
            return []
        output_division_lists = []
        depths = self._get_depths()
        for i, input_division in enumerate(input_divisions):
            input_division = durationtools.Division(input_division)
            depth = depths[i]
            meter = metertools.Meter(
                input_division,
                decrease_durations_monotonically=\
                    self.decrease_durations_monotonically,
                )
            durations = meter.get_durations_at_depth(depth)
            denominator = input_division.denominator
            output_division_list = [
                durationtools.Division(_.with_denominator(denominator))
                for _ in durations
                ]
            output_division_lists.append(output_division_list)
        return output_division_lists

    ### PRIVATE METHODS ###

    def _get_depths(self):
        if self.depths:
            depths = self.depths
        else:
            depths = (1,)
        depths = datastructuretools.CyclicTuple(depths)
        return depths

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        r'''Is true when beat-group durations should decrease monotonically.
        Otherwise false.

        ..  container:: example

            **Example 1.** Decreases beat-group durations monotonically:

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     decrease_durations_monotonically=True,
            ...     depths=[1],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(3, 4), Division(2, 4), Division(2, 4)]
            [Division(3, 4), Division(3, 4)]
            [Division(3, 4), Division(2, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

            This is default behavior.

        ..  container:: example

            **Example 2.** Increases beat-group durations monotonically:

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     decrease_durations_monotonically=False,
            ...     depths=[1],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(2, 4), Division(2, 4), Division(3, 4)]
            [Division(3, 4), Division(3, 4)]
            [Division(2, 4), Division(3, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

        Set to true or false.
        '''
        return self._decrease_durations_monotonically

    @property
    def depths(self):
        r'''Gets depths of beat division maker.

        ..  container:: example

            **Example 1.** Gets durations at depth ``0``:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker(
                ...     depths=[0],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(7, 4)]
                [Division(6, 4)]

            Output equals input.

        ..  container:: example

            **Example 2.** Gets durations at depth ``1``:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker(
                ...     depths=[1],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(3, 4), Division(2, 4), Division(2, 4)]
                [Division(3, 4), Division(3, 4)]

            Output equals beat-group durations.

            This is default behavior when `depths` is not set.

        ..  container:: example

            **Example 3.** Gets durations at depth ``2``:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker(
                ...     depths=[2],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

        ..  container:: example

            **Example 4.** Gets durations at depths ``0`` and ``1`` 
            alternately:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker(
                ...     depths=[0, 1],
                ...     )
                >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(7, 4)]
                [Division(3, 4), Division(3, 4)]
                [Division(5, 4)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

        Set to nonnegative integers or none.
        '''
        return self._depths