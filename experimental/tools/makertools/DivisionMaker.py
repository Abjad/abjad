# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class DivisionMaker(AbjadValueObject):
    r'''NonreducedFraction-maker.

    ..  container:: example

        **Example 1.** Splits every division by ``1/4`` with remainder at 
        right:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
            [NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
            [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]


        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
            >>> divisions = sequencetools.flatten_sequence(division_lists)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=input_divisions,
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
                    \time 3/8
                    c'4
                    c'8
                }
                {
                    \time 5/8
                    c'4
                    c'4
                    c'8
                }
            }

    ..  container:: example

        **Example 2a.** Fuses divisions:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=mathtools.Infinity,
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = division_maker(input_divisions)
            >>> divisions
            [NonreducedFraction(15, 8)]


        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=input_divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                c'1...
            }

        **Example 2b.** Fuses divisions and then splits by ``1/4`` with
        remainder on right:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=mathtools.Infinity,
            ...     )
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
            >>> divisions = sequencetools.flatten_sequence(division_lists)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=input_divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP


        ..  doctest::

            >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'8
            }

    ..  container:: example

        **Example 3a.** Splits every division by ``3/8``:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 8)],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [NonreducedFraction(3, 8), NonreducedFraction(3, 8), NonreducedFraction(1, 8)]
            [NonreducedFraction(3, 8)]
            [NonreducedFraction(3, 8), NonreducedFraction(1, 4)]

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
            >>> divisions = sequencetools.flatten_sequence(division_lists)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=input_divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 7/8
                    c'4.
                    c'4.
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
                {
                    \time 5/8
                    c'4.
                    c'4
                }
            }

        **Example 3b.** Splits every division by ``3/8`` and then fuses
        flattened divisions into differently sized groups:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 8)],
            ...     )
            >>> division_maker = division_maker.flatten()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2, 3, 1],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = division_maker(input_divisions)
            >>> divisions
            [NonreducedFraction(6, 8), NonreducedFraction(7, 8), NonreducedFraction(1, 4)]

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=input_divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                c'2.
                c'2..
                c'4
            }

    NonreducedFraction-makers object-model a sequence of partially evaluated functions 
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
            expr = [mathtools.NonreducedFraction(_) for _ in expr]
        for callback in self.callbacks:
            expr = callback(expr)
        return expr

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = new(self)
        result._callbacks = callbacks
        return result

    @staticmethod
    def _is_flat_list(expr):
        if isinstance(expr, list):
            if not(expr):
                return True
            elif not isinstance(expr[0], list):
                return True
        return False

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
                (SplitByDurationsDivisionCallback(compound_meter_multiplier=Multiplier(1, 1), durations=(NonreducedFraction(1, 4),)),)

        Returns tuple of zero or more callbacks.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def append_callback(self, callback):
        r'''Configures division-maker with arbitrary `callback`.

        Returns new division-maker.
        '''
        return self._append_callback(callback)

    def flatten(self, depth=-1):
        r'''Flattens division lists.

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.FlattenDivisionCallback(depth=depth)
        return self._append_callback(callback)

    def fuse_by_counts(
        self,
        cyclic=True,
        counts=None,
        ):
        r'''Fuses divisions (or division lists) by `counts`.

        ..  container:: example

            **Example 1.** Fuses every two divisions together:
 
            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )

            ::

                >>> input_divisions = [(7, 8), (7, 8), (7, 16)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [NonreducedFraction(14, 8), NonreducedFraction(7, 16)]

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=input_divisions,
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
        return self._append_callback(callback)

    def partition_by_counts(
        self,
        counts=None,
        fuse_assignable_total_duration=False,
        append_remainder=False,
        remainder_direction=Right,
        ):
        r'''Partitions divisions (or division lists) by `counts`.

        ..  container:: example

            **Example 1a.** Partitions divisions into pairs with remainder at
            right:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> division_list = division_maker(divisions)
                >>> division_list
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8)], [NonreducedFraction(1, 4), NonreducedFraction(1, 4)], [NonreducedFraction(1, 16)]]

            **Example 1b.** Partitions divisions into pairs with remainder
            appended at right:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> division_list = division_maker(divisions)
                >>> division_list
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8)], [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 16)]]

            **Example 1c.** Partitions divisions into pairs with remainder at
            left:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> division_list = division_maker(divisions)
                >>> division_list
                [[NonreducedFraction(1, 8)], [NonreducedFraction(1, 8), NonreducedFraction(1, 4)], [NonreducedFraction(1, 4), NonreducedFraction(1, 16)]]

            **Example 1d.** Partitions divisions into pairs with remainder
            appeneded at left:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> division_list = division_maker(divisions)
                >>> division_list
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8), NonreducedFraction(1, 4)], [NonreducedFraction(1, 4), NonreducedFraction(1, 16)]]

            These examples show how the class partitions a flat list of
            divisions. Output equal to one nested division list.

        ..  container:: example

            **Example 2a.** Partitions division lists into pairs with
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
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8)], [NonreducedFraction(1, 4)]]
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8)], [NonreducedFraction(1, 4), NonreducedFraction(1, 4)], [NonreducedFraction(1, 16)]]

            **Example 2b.** Partitions division lists into pairs with
            remainders appended at right:

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
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]]
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8)], [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 16)]]

            **Example 2c.** Partitions division lists into pairs with
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
                [[NonreducedFraction(1, 8)], [NonreducedFraction(1, 8), NonreducedFraction(1, 4)]]
                [[NonreducedFraction(1, 8)], [NonreducedFraction(1, 8), NonreducedFraction(1, 4)], [NonreducedFraction(1, 4), NonreducedFraction(1, 16)]]

            **Example 2d.** Partitions division lists into pairs with
            remainders appended at left:

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
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]]
                [[NonreducedFraction(1, 8), NonreducedFraction(1, 8), NonreducedFraction(1, 4)], [NonreducedFraction(1, 4), NonreducedFraction(1, 16)]]

            These examples show how the class automatically maps over multiple
            input division lists. Output equal to arbitrarily many nested
            division lists.

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.PartitionDivisionCallback(
            counts=counts,
            fuse_assignable_total_duration=fuse_assignable_total_duration,
            append_remainder=append_remainder,
            remainder_direction=remainder_direction,
            )
        return self._append_callback(callback)

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
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
                [NonreducedFraction(1, 4), NonreducedFraction(3, 16)]

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
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]
                [NonreducedFraction(3, 16), NonreducedFraction(1, 4)]

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
        return self._append_callback(callback)

    def split_by_rounded_ratios(
        self,
        ratios=None,
        ):
        r'''Splits divisions by rounded ratios.

        ..  container:: example

            **Example 1.** Makes divisions with ``2:1`` ratios:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.split_by_rounded_ratios(
                ...     ratios=[mathtools.Ratio([2, 1])],
                ...     )

            ::

                >>> input_divisions = [(5, 8), (6, 8)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [NonreducedFraction(3, 8), NonreducedFraction(2, 8)]
                [NonreducedFraction(4, 8), NonreducedFraction(2, 8)]

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=input_divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4.
                        c'4
                    }
                    {
                        \time 6/8
                        c'2
                        c'4
                    }
                }


        ..  container:: example

            **Example 2.** Makes divisions with alternating ``2:1`` and 
            ``1:1:1`` ratios:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.split_by_rounded_ratios(
                ...     ratios=[
                ...         mathtools.Ratio([2, 1]),
                ...         mathtools.Ratio([1, 1, 1]),
                ...         ],
                ...     )

            ::

                >>> input_divisions = [(5, 8), (6, 8)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [NonreducedFraction(3, 8), NonreducedFraction(2, 8)]
                [NonreducedFraction(2, 8), NonreducedFraction(2, 8), NonreducedFraction(2, 8)]

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=input_divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4.
                        c'4
                    }
                    {
                        \time 6/8
                        c'4
                        c'4
                        c'4
                    }
                }

        Returns new division-maker.
        '''
        from experimental.tools import makertools
        callback = makertools.SplitByRoundedRatiosDivisionCallback(
            ratios=ratios,
            )
        return self._append_callback(callback)