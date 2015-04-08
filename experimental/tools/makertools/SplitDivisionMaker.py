# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import new


class SplitDivisionMaker(AbjadValueObject):
    r'''Division-maker.

    ..  container:: example

        **Example 1.** Makes quarter-valued divisions with remainder at right:

        ::

            >>> maker = makertools.SplitDivisionMaker(durations=[(1, 4)])

        ::

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> division_lists = maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
            [Division(1, 4), Division(3, 16)]

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()
            >>> divisions = sequencetools.flatten_sequence(division_lists)
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=time_signatures,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
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

        **Example 2.** Makes quarter-valued divisions with remainder at left:

        ::

            >>> maker = makertools.SplitDivisionMaker(
            ...     durations=[(1, 4)],
            ...     remainder=Left,
            ...     )

        ::

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> division_lists = maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(1, 8), Division(1, 4), Division(1, 4), Division(1, 4)]
            [Division(1, 8), Division(1, 4), Division(1, 4), Division(1, 4)]
            [Division(3, 16), Division(1, 4)]

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()
            >>> divisions = sequencetools.flatten_sequence(division_lists)
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     time_signatures=time_signatures,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
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

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output. Output structured one output list per input
    division.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callbacks',
        '_cyclic',
        '_pattern',
        '_pattern_rotation_index',
        '_remainder',
        '_remainder_fuse_threshold',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=Right,
        remainder_fuse_threshold=None,
        ):
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        durations = durations or ()
        pattern_ = []
        for division in durations:
            division = durationtools.Division(division)
            pattern_.append(division)
        durations = tuple(pattern_)
        self._pattern = durations
        assert remainder in (Left, Right), repr(remainder)
        self._remainder = remainder
        assert isinstance(pattern_rotation_index, int)
        self._pattern_rotation_index = pattern_rotation_index
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = durationtools.Duration(
                remainder_fuse_threshold,
                )
        self._remainder_fuse_threshold = remainder_fuse_threshold
        self._callbacks = ()

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls division-maker on `divisions`.

        ..  container:: example

            **Example 1.** Division without remainder:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(3, 4)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(1, 4), Division(1, 4)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    }
                }

        ..  container:: example

            **Example 2.** Division with remainder:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 8)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list 
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                }

            Positions remainder at right of output because divison-maker
            `remainder` defaults to right.

        ..  container:: example

            **Example 3.** Multiple divisions:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(2, 4), (3, 4)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(1, 4)]
                [Division(1, 4), Division(1, 4), Division(1, 4)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 2/4
                        c'4
                        c'4
                    }
                    {
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    }
                }

        ..  container:: example

            **Example 4.** No durations:

            ::

                >>> maker = makertools.SplitDivisionMaker()

            ::

                >>> time_signatures = [(6, 32)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(6, 32)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 6/32
                        c'8.
                    }
                }

            Returns input division unchanged.

        ..  container:: example

            **Example 5.** Empty input:

            ::

                >>> maker = makertools.SplitDivisionMaker(durations=[(1, 4)])
                >>> maker()
                []

            Returns empty list.

        Returns possibly empty list of division lists.
        '''
        divisions = divisions or []
        if not divisions:
            return []
        division_lists = []
        for i, division in enumerate(divisions):
            input_division = durationtools.Division(division)
            input_duration = durationtools.Duration(input_division)
            assert 0 < input_division, repr(input_division)
            if not self.durations:
                division_list = [input_division]
                division_lists.append(division_list)
                continue
            division_list = list(self.durations)
            pattern_rotation_index = self.pattern_rotation_index or 0
            pattern_rotation_index *= i
            division_list = sequencetools.rotate_sequence(
                division_list,
                pattern_rotation_index,
                )
            if self.cyclic:
                division_list = sequencetools.repeat_sequence_to_weight(
                    division_list,
                    input_division,
                    allow_total=Less,
                    )
            total_duration = durationtools.Duration(sum(division_list))
            if total_duration == input_duration:
                division_lists.append(division_list)
                continue
            if self.remainder is None:
                message = 'can not fill {} from {} exactly.'
                message = message.format(input_division, self.durations)
                raise Exception(message)
            remainder = input_division - total_duration
            remainder = durationtools.Duration(remainder)
            remainder = durationtools.Division(remainder)
            if self.remainder == Left:
                if self.remainder_fuse_threshold is None:
                    division_list.insert(0, remainder)
                elif remainder <= self.remainder_fuse_threshold:
                    fused_value = division_list[0] + remainder
                    fused_value = durationtools.Division(fused_value)
                    division_list[0] = fused_value
                else:
                    division_list.insert(0, remainder)
            elif self.remainder == Right:
                if self.remainder_fuse_threshold is None:
                    division_list.append(remainder)
                elif remainder <= self.remainder_fuse_threshold:
                    fused_value = division_list[-1] + remainder
                    fused_value = durationtools.Division(fused_value)
                    division_list[-1] = fused_value
                else:
                    division_list.append(remainder)
            else:
                raise ValueError((self.remainder, remainder))
            total_duration = durationtools.Duration(sum(division_list))
            pair = total_duration, input_duration
            assert total_duration == input_duration, pair
            division_lists.append(division_list)
        callbacks = self.callbacks or ()
        for callback in callbacks:
            divisions = sequencetools.flatten_sequence(division_lists)
            division_lists = callback(divisions)
        return division_lists

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        if self.cyclic == True:
            keyword_argument_names.remove('cyclic')
        if not self.durations:
            keyword_argument_names.remove('durations')
        if self.remainder == Right:
            keyword_argument_names.remove('remainder')
        if self.pattern_rotation_index == 0:
            keyword_argument_names.remove('pattern_rotation_index')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

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
        r'''Gets callbacks of division-maker.

        ..  container:: example

            **Example 1.** Without fuse callback:

            ::

                >>> division_maker = makertools.SplitDivisionMaker(durations=[(1, 4)])

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

            **Example 2.** With fuse callback:

            ::

                >>> division_maker = makertools.SplitDivisionMaker(durations=[(1, 4)])
                >>> division_maker = division_maker.fuse(counts=[2, 4])

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(2, 4)]
                [Division(7, 8)]
                [Division(3, 8)]
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
                    c'2
                    c'2..
                    c'4.
                    c'4..
                }
                    
        '''
        return self._callbacks

    @property
    def cyclic(self):
        r'''Is true when division-maker reads durations cyclically for each input
        division.
        
        Is false when division-maker reads durations only once per input
        division.

        ..  container:: example

            **Example 1.** Reads durations cyclically for each input division:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(3, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
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

            **Example 2.** Reads durations only once per input division:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=False,
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(5, 8)]
                [Division(1, 4), Division(5, 8)]
                [Division(1, 4), Division(3, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'4
                        c'2 ~
                        c'8
                    }
                    {
                        c'4
                        c'2 ~
                        c'8
                    }
                    {
                        \time 7/16
                        c'4
                        c'8.
                    }
                }

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._cyclic

    @property
    def durations(self):
        r'''Gets durations of division-maker.

        ..  container:: example

            **Example 1.** Returns input division unchanged when durations is
            empty:

                >>> maker = makertools.SplitDivisionMaker()

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(7, 8)]
                [Division(7, 8)]
                [Division(7, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
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

            **Example 2.** Applies durations to each input division:

                >>> maker = makertools.SplitDivisionMaker(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(3, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
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

        Defaults to none.

        Set to durations or none.

        Returns durations or none.
        '''
        return self._pattern

    @property
    def pattern_rotation_index(self):
        r'''Gets durations rotation index of division-maker.

        ..  container:: example

            **Example 1.** Does not rotate durations:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 16), (1, 8), (1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 16), Division(1, 8), Division(1, 4)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'16
                        c'8
                        c'4
                    }
                    {
                        c'16
                        c'8
                        c'4
                    }
                    {
                        c'16
                        c'8
                        c'4
                    }
                }

        ..  container:: example

            **Example 2.** Rotates durations one element to the left on each new
            input division:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 16), (1, 8), (1, 4)],
                ...     pattern_rotation_index=-1,
                ...     )

            ::

                >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
                >>> division_lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 8), Division(1, 4), Division(1, 16)]
                [Division(1, 4), Division(1, 16), Division(1, 8)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'16
                        c'8
                        c'4
                    }
                    {
                        c'8
                        c'4
                        c'16
                    }
                    {
                        c'4
                        c'16
                        c'8
                    }
                }

        ..  container:: example

            **Example 3.** Rotates durations one element to the right on each new
            input division:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 16), (1, 8), (1, 4)],
                ...     pattern_rotation_index=1,
                ...     )

            ::

                >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 4), Division(1, 16), Division(1, 8)]
                [Division(1, 8), Division(1, 4), Division(1, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'16
                        c'8
                        c'4
                    }
                    {
                        c'4
                        c'16
                        c'8
                    }
                    {
                        c'8
                        c'4
                        c'16
                    }
                }

        Defaults to 0.

        Set to integer.

        Returns integer.
        '''
        return self._pattern_rotation_index

    @property
    def remainder(self):
        r'''Gets direction to which any remainder will be positioned.

        ..  container:: example

            **Example 1.** Positions remainder to right of noncyclic durations:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=False,
                ...     durations=[(4, 16), (1, 16)],
                ...     )

            ::

                >>> time_signatures = [(3, 4)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(4, 16), Division(1, 16), Division(7, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4
                        c'16
                        c'4..
                    }
                }

        ..  container:: example

            **Example 2.** Positions remainder to right of cyclic durations:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     durations=[(4, 16), (1, 16)],
                ...     )

            ::

                >>> time_signatures = [(3, 4)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(4, 16), Division(1, 16), Division(4, 16), Division(1, 16), Division(1, 8)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4
                        c'16
                        c'4
                        c'16
                        c'8
                    }
                }

        ..  container:: example

            **Example 3.** Positions remainder to left of noncyclic durations:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=False,
                ...     durations=[(1, 4), (1, 16)],
                ...     remainder=Left,
                ...     )

            ::

                >>> time_signatures = [(3, 4)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(7, 16), Division(1, 4), Division(1, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4..
                        c'4
                        c'16
                    }
                }

        ..  container:: example

            **Example 4.** Positions remainder to left of cyclic durations:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 4), (1, 16)],
                ...     remainder=Left,
                ...     )

            ::

                >>> time_signatures = [(3, 4)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 8), Division(1, 4), Division(1, 16), Division(1, 4), Division(1, 16)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'8
                        c'4
                        c'16
                        c'4
                        c'16
                    }
                }

        Defaults to right.

        Set to left or right.

        Returns left or right.
        '''
        return self._remainder

    @property
    def remainder_fuse_threshold(self):
        r'''Gets remainder fuse threshold of division-maker.

        ..  container:: example

            **Example 1.** No threshold. Remainder unfused to the right:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     durations=[(1, 4)],
                ...     remainder_fuse_threshold=None,
                ...     )

            ::

                >>> time_signatures = [(5, 8)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(1, 4), Division(1, 8)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4
                        c'4
                        c'8
                    }
                }

        ..  container:: example

            **Example 2.** Remainder less than or equal to ``1/8`` fused 
            to the right:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     durations=[(1, 4)],
                ...     remainder_fuse_threshold=Duration(1, 8),
                ...     )

            ::

                >>> time_signatures = [(5, 8)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 4), Division(3, 8)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4
                        c'4.
                    }
                }

        ..  container:: example

            **Example 3.** No threshold. Remainder unfused to the left:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 4)],
                ...     remainder=Left,
                ...     remainder_fuse_threshold=None,
                ...     )

            ::

                >>> time_signatures = [(5, 8)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 8), Division(1, 4), Division(1, 4)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'8
                        c'4
                        c'4
                    }
                }

        ..  container:: example

            **Example 4.** Remainder less than or equal to ``1/8`` fused to the
            left:

            ::

                >>> maker = makertools.SplitDivisionMaker(
                ...     cyclic=True,
                ...     durations=[(1, 4)],
                ...     remainder=Left,
                ...     remainder_fuse_threshold=Duration(1, 8),
                ...     )

            ::

                >>> time_signatures = [(5, 8)]
                >>> division_lists = maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(3, 8), Division(1, 4)]

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = sequencetools.flatten_sequence(division_lists)
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     time_signatures=time_signatures,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4.
                        c'4
                    }
                }

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._remainder_fuse_threshold

    ### PUBLIC METHODS ###

    def fuse(
        self,
        cyclic=True,
        counts=None,
        ):
        from experimental.tools import makertools
        callback = makertools.FuseByCountsDivisionCallback(
            cyclic=cyclic,
            measure_counts=counts,
            )
        return self._with_callback(callback)