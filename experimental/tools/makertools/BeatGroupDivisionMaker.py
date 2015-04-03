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

        **Example 1.** Makes measure-durated divisions:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker()
            >>> meters = [(4, 4), (5, 4), (6, 4), (7, 4)]
            >>> division_lists = maker(meters)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(1, 1)]
            [Division(5, 4)]
            [Division(3, 2)]
            [Division(7, 4)]

    ..  container:: example

        **Example 2.** Makes beat-durated divisions:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     beat_maker=rhythmmakertools.DurationBeatMaker(
            ...         compound_beat_duration=Duration(3, 8),
            ...         simple_beat_duration=Duration(1, 4),
            ...         ),
            ...     beat_grouper=rhythmmakertools.BeatGrouper(
            ...         counts=[1],
            ...         ),
            ...     )
            >>> meters = [(4, 4), (5, 4), (6, 4), (7, 4)]
            >>> division_lists = maker(meters)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]
            [Division(3, 8), Division(3, 8), Division(3, 8), Division(3, 8)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 4)]

    ..  container:: example

        **Example 3.** Makes beat-group-durated divisions:

        ::

            >>> maker = makertools.BeatGroupDivisionMaker(
            ...     beat_grouper=rhythmmakertools.BeatGrouper(
            ...         counts=[2],
            ...         fuse_remainder=True,
            ...         remainder_direction=Right,
            ...     ),
            ...     beat_maker=rhythmmakertools.DurationBeatMaker(
            ...         compound_beat_duration=Duration(3, 8),
            ...         simple_beat_duration=Duration(1, 4),
            ...         ),
            ...     )
            >>> meters = [(4, 4), (5, 4), (6, 4), (7, 4)]
            >>> division_lists = maker(meters)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(1, 2), Division(1, 2)]
            [Division(1, 2), Division(3, 4)]
            [Division(3, 4), Division(3, 4)]
            [Division(1, 2), Division(1, 2), Division(3, 4)]

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output. Ouput is structured one output list per input
    division.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_beat_grouper',
        '_beat_maker',
        '_decrease_durations_monotonically',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beat_grouper=None,
        beat_maker=None,
        decrease_durations_monotonically=True,
        ):
        self._beat_grouper = beat_grouper
        self._beat_maker = beat_maker
        prototype = (type(None), type(True))
        assert isinstance(decrease_durations_monotonically, prototype)
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls beat group division maker on `divisions`.

        ..  container:: example

            **Example 1.** Calls maker on empty input:

            ::

                >>> maker = makertools.BeatGroupDivisionMaker()
                >>> division_lists = maker([])
                >>> division_lists
                []

            Returns empty list.

        Returns (possibly empty) list of division lists.
        '''
        input_divisions = divisions or []
        if not input_divisions:
            return []
        output_division_lists = []
        meters = []
        for input_division in input_divisions:
            meter = metertools.Meter(
                input_division,
                decrease_durations_monotonically=\
                    self.decrease_durations_monotonically,
                )
            meters.append(meter)
        beat_lists = []
        for meter in meters:
            beat_list = self._get_beat_maker()([meter])[0]
            beat_lists.append(beat_list)
        grouped_beat_lists = []
        for beat_list in beat_lists:
            grouped_beat_list = self._get_beat_grouper()([beat_list])[0]
            grouped_beat_lists.append(grouped_beat_list)
        group_durations = []
        for grouped_beat_list in grouped_beat_lists:
            group_durations_ = [sum(_) for _ in grouped_beat_list]
            output_division_list = [
                durationtools.Division(_) for _ in group_durations_]
            output_division_lists.append(output_division_list)
        return output_division_lists

    ### PRIVATE METHODS ###

    def _get_beat_grouper(self):
        from abjad.tools import rhythmmakertools
        if self.beat_grouper is not None:
            return self.beat_grouper
        grouper = rhythmmakertools.BeatGrouper()
        return grouper

    def _get_beat_maker(self):
        from abjad.tools import rhythmmakertools
        if self.beat_maker is not None:
            return self.beat_maker
        maker = rhythmmakertools.DurationBeatMaker()
        return maker

    ### PUBLIC PROPERTIES ###

    @property
    def beat_grouper(self):
        r'''Gets beat grouper of division maker.

        Returns beat grouper or none.
        '''
        return self._beat_grouper

    @property
    def beat_maker(self):
        r'''Gets beat maker of division maker.

        Returns beat maker or none.
        '''
        return self._beat_maker

    @property
    def decrease_durations_monotonically(self):
        r'''Is true when beat-group durations should decrease monotonically.
        Otherwise false.

        Set to true or false.
        '''
        return self._decrease_durations_monotonically