# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class DivisionMaker(AbjadValueObject):
    r'''Division-maker.

    ..  container:: example

        **Example 1.** Makes divisions:

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

        **Example 2.** Makes quarter-valued divisions with remainder at 
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

    Division-makers object-model a sequence of partially evaluated functions 
    taken together in functional composition.

    Usage follows the two-step configure-once / call-repeatedly pattern shown 
    here.
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

    def __call__(self, expr=None):
        r'''Makes divisions from `expr`.

        Pass in `expr` as either a list of divisions or as a list of division
        lists.

        Returns either a list of divisions or a list of division lists.
        '''
        expr = expr or []
        expr = list(expr)
        assert isinstance(expr, list), repr(expr)
        if self._is_flat_list(expr):
            expr = [durationtools.Division(_) for _ in expr]
        for callback in self.callbacks:
            expr = callback(expr)
        return expr

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_flat_list(expr):
        if isinstance(expr, list):
            if not(expr):
                return True
            elif not isinstance(expr[0], list):
                return True
        return False

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

        ..  container:: example

            **Example 1.** No callbacks:

            ::

                >>> division_maker = makertools.DivisionMaker()

            ::

                >>> division_maker.callbacks
                ()

        ..  container:: example

            **Example 2.** One callback:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> division_maker.callbacks
                (SplitByDurationsDivisionCallback(compound_meter_multiplier=Multiplier(1, 1), durations=(Division(1, 4),)),)

        Returns tuple of zero or more callbacks.
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

    def partition_by_counts(
        self,
        counts=None,
        fuse_assignable_total_duration=False,
        append_remainder=False,
        remainder_direction=Right,
        ):
        r'''Partitions divisions by `counts`.

        ..  container:: example

            **Example 1a.** Partitions division lists into pairs with
            remainders at right:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                [[Division(1, 8), Division(1, 8)], [Division(1, 4)]]
                [[Division(1, 8), Division(1, 8)], [Division(1, 4), Division(1, 4)], [Division(1, 16)]]

            **Example 1b.** Partitions division lists into pairs with
            remainders at left:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                [[Division(1, 8)], [Division(1, 8), Division(1, 4)]]
                [[Division(1, 8)], [Division(1, 8), Division(1, 4)], [Division(1, 4), Division(1, 16)]]

        ..  container:: example

            **Example 2a.** Partitions division lists into pairs with
            remainders fused at right:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                [[Division(1, 8), Division(1, 8), Division(1, 4)]]
                [[Division(1, 8), Division(1, 8)], [Division(1, 4), Division(1, 4), Division(1, 16)]]

            **Example 2b.** Partitions division lists into pairs with
            remainders fused at left:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                [[Division(1, 8), Division(1, 8), Division(1, 4)]]
                [[Division(1, 8), Division(1, 8), Division(1, 4)], [Division(1, 4), Division(1, 16)]]

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.PartitionDivisionCallback(
            counts=counts,
            fuse_assignable_total_duration=fuse_assignable_total_duration,
            append_remainder=append_remainder,
            remainder_direction=remainder_direction,
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