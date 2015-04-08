# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class DivisionMaker(AbjadValueObject):
    r'''A division-maker.

    ..  container:: example

        **Example 1.** Makes divisions:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> divisions = [(4, 8), (3, 8), (4, 8), (2, 8)]
            >>> division_maker(divisions)
            [Division(4, 8), Division(3, 8), Division(4, 8), Division(2, 8)]

    Division-makers aggregate a sequence of callable classes which describe the
    process of making (fusing, splitting, partitioning) divisions (arbitrary
    units of musical time).

    Division-makers provide methods for configuring and making new selectors.

    Composers may chain division-makers together.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callbacks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        callbacks=None,
        ):
        callbacks = callbacks or ()
        if callbacks:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Makes divisions from `divisions`.

        Returns a (possibly empty) list of division lists.
        '''
        divisions = [durationtools.Division(_) for _ in divisions]
        for callback in self.callbacks:
            divisions = callback(divisions)
        return divisions

    ### PRIVATE METHODS ###

    def _with_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = new(self)
        result._callbacks = callbacks
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets division-maker callbacks.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def fuse_by_counts(
        self,
        cyclic=True,
        counts=None,
        ):
        r'''Fuses divisions by `counts`.

        ..  container:: example

            **Example 1.** Fuses nothing:
 
            ::

                >>> division_maker = makertools.DivisionMaker()

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> divisions = division_maker(time_signatures)
                >>> for division in divisions:
                ...     division
                Division(7, 8)
                Division(7, 8)
                Division(7, 16)

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'2..
                    }
                    {
                        c'2..
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                }

        ..  container:: example

            **Example 2.** Fuses every two divisions together:
 
            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(14, 8)]
                [Division(7, 16)]

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    c'1..
                    c'4..
                }

        '''
        from experimental.tools import makertools
        callback = makertools.FuseByCountsDivisionCallback(
            cyclic=cyclic,
            counts=counts,
            )
        return self._with_callback(callback)

    # TODO: remove?
#    def partition(
#        self,
#        counts=None,
#        fuse_assignable_total_duration=False,
#        fuse_remainder=False,
#        remainder_direction=Right,
#        ):
#        r'''Partitions divisions by `counts`.
#
#        ..  todo:: Add examples.
#
#        Returns new division-maker.
#        '''
#        from experimental.tools import makertools
#        callback = makertools.PartitionDivisionCallback(
#            counts=counts,
#            fuse_assignable_total_duration=fuse_assignable_total_duration,
#            fuse_remainder=fuse_remainder,
#            remainder_direction=remainder_direction,
#            )
#        return self._with_callback(callback)

    def split_by_beats(
        self, 
        compound_beat_duration=None,
        fuse_remainder=False,
        remainder_direction=Right,
        simple_beat_duration=None,
        ):
        r'''Splits divisions by beats.

        ..  todo:: Add examples.

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.SplitByBeatsDivisionCallback(
            compound_beat_duration=compound_beat_duration,
            fuse_remainder=fuse_remainder,
            remainder_direction=remainder_direction,
            simple_beat_duration=simple_beat_duration,
            )
        return self._with_callback(callback)

    def split_by_durations(
        self,
        compound_meter_multiplier=durationtools.Multiplier(1),
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=Right,
        remainder_fuse_threshold=None,
        ):
        r'''Splits divisions by durations.

        ..  container:: example

            **Example 1.** Makes quarter-valued divisions with remainder at 
            right:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(3, 16)]

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                    {
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                    {
                        \time 7/16
                        c'4
                        c'8.
                    }
                }

        ..  container:: example

            **Example 2.** Makes quarter-valued divisions with remainder at 
            left:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(1, 4)],
                ...     remainder=Left,
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 8), Division(1, 4), Division(1, 4), Division(1, 4)]
                [Division(1, 8), Division(1, 4), Division(1, 4), Division(1, 4)]
                [Division(3, 16), Division(1, 4)]

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'8
                        c'4
                        c'4
                        c'4
                    }
                    {
                        c'8
                        c'4
                        c'4
                        c'4
                    }
                    {
                        \time 7/16
                        c'8.
                        c'4
                    }
                }

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.SplitByDurationsDivisionCallback(
            compound_meter_multiplier=compound_meter_multiplier,
            cyclic=cyclic,
            durations=durations,
            pattern_rotation_index=pattern_rotation_index,
            remainder=remainder,
            remainder_fuse_threshold=remainder_fuse_threshold,
            )
        return self._with_callback(callback)

    def split_by_rounded_ratios(
        self,
        ratios=None,
        ):
        r'''Splits divisions by rounded ratios.

        ..  todo:: Add examples.

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.SplitByBeatsDivisionCallback(
            ratios=ratios,
            )
        return self._with_callback(callback)

    def with_callback(self, callback):
        r'''Configures division-maker with arbitrary `callback`.

        Returns new division-maker.
        '''
        return self._with_callback(callback)