# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class FuseByCountsDivisionCallback(AbjadValueObject):
    r'''Fuse-by-counts division callback.

    ..  container:: example

        **Example 1.** Fuses divisions together two at a time:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2],
            ...     )

        ::

            >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> divisions = division_maker(input_divisions)
            >>> divisions
            [NonreducedFraction(4, 8), NonreducedFraction(8, 8), NonreducedFraction(2, 4)]

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
                c'2
                c'1
                c'2
            }

    ..  container:: example

        **Example 2.** Fuses divisions together two at a time. Then splits
        resulting divisions by ``3/16`` durations:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2],
            ...     )
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[Duration(3, 16)],
            ...     remainder=Right,
            ...     )

        ::

            >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 8)]
            [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 16)]
            [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 8)]


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
                c'8.
                c'8.
                c'8
                c'8.
                c'8.
                c'8.
                c'8.
                c'8.
                c'16
                c'8.
                c'8.
                c'8
            }

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output.

    Treats input as time signatures. Glues input together into hypermeasures
    according to optional measure counts. Postprocesses resulting
    hypermeasures with optional secondary division maker.

    Follows the two-step configure-once / call-repeatly pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cyclic',
        '_counts',
        '_secondary_division_maker',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=True,
        counts=None,
        secondary_division_maker=None,
        ):
        from experimental import makertools
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        counts = counts or ()
        if (counts == mathtools.Infinity or 
            counts == mathtools.Infinity()):
            self._counts = counts
        else:
            assert mathtools.all_are_positive_integers(counts)
            self._counts = counts
        if secondary_division_maker is not None:
            prototype = (makertools.SplitByDurationsDivisionCallback,)
            assert isinstance(secondary_division_maker, prototype)
        self._secondary_division_maker = secondary_division_maker

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls fuse-by-counts division callback.

        ..  container:: example

            **Example 1.** Returns divisions unfused:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts()

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [NonreducedFraction(2, 8), NonreducedFraction(2, 8), NonreducedFraction(4, 8), NonreducedFraction(4, 8), NonreducedFraction(2, 4)]

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
                    {
                        \time 2/8
                        c'4
                    }
                    {
                        c'4
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        c'2
                    }
                    {
                        \time 2/4
                        c'2
                    }
                }

        ..  container:: example

            **Example 2.** Fuses divisions two at a time:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [NonreducedFraction(4, 8), NonreducedFraction(8, 8), NonreducedFraction(2, 4)]

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
                    c'2
                    c'1
                    c'2
                }

        ..  container:: example

            **Example 3a.** Fuses divisions two at a time.
            Then splits fused divisions by ``3/16`` durations.

            Remainders to the right:
            
            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[Duration(3, 16)],
                ...     remainder=Right,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 8)]
                [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 16)]
                [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 8)]

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
                    c'8.
                    c'8.
                    c'8
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'16
                    c'8.
                    c'8.
                    c'8
                }

            **Example 3b.** Remainders to the left:
            
            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[Duration(3, 16)],
                ...     remainder=Left,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [NonreducedFraction(1, 8), NonreducedFraction(3, 16), NonreducedFraction(3, 16)]
                [NonreducedFraction(1, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16)]
                [NonreducedFraction(1, 8), NonreducedFraction(3, 16), NonreducedFraction(3, 16)]

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
                    c'8
                    c'8.
                    c'8.
                    c'16
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8
                    c'8.
                    c'8.
                }

        ..  container:: example

            **Example 4.** Fuses all divisions:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=mathtools.Infinity,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [NonreducedFraction(16, 8)]

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
                    c'\breve
                }

        ..  container:: example

            **Example 5a.** Fuses all divisions. Then splits fused divisions
            by ``3/8`` durations:

            Remainder at right:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=mathtools.Infinity,
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[Duration(3, 16)],
                ...     remainder=Right,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 8)]

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
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8
                }

            **Example 5b.** Remainder at left:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=mathtools.Infinity,
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[Duration(3, 16)],
                ...     remainder=Left,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [NonreducedFraction(1, 8), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16)]

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
                    c'8
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                }

        ..  container:: example

            **Example 6.** Empty input:

            ::

                >>> input_divisions = []
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list

        Returns list of division lists.
        '''
        divisions = divisions or ()
        divisions = self._coerce_divisions(divisions)
        if not divisions:
            pass
        elif (self.counts == mathtools.Infinity or 
            self.counts == mathtools.Infinity()):
            divisions = [sum(divisions)]
        elif self.counts:
            parts = sequencetools.partition_sequence_by_counts(
                divisions,
                self.counts,
                cyclic=self.cyclic,
                overhang=True,
                )
            divisions = [sum(_) for _ in parts]
        divisions = [mathtools.NonreducedFraction(_) for _ in divisions]
        if self.secondary_division_maker is None:
            return divisions
        division_lists = []
        for division in divisions:
            if self.secondary_division_maker is not None:
                division_list = self.secondary_division_maker([division])[0]
            else:
                division_list = [division]
            division_list = [mathtools.NonreducedFraction(_) for _ in division_list]
            division_lists.append(division_list)
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
        if not self.counts:
            keyword_argument_names.remove('counts')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PRIVATE METHODS ###

    def _coerce_divisions(self, divisions):
        nonreduced_fractions = []
        for division in divisions:
            if hasattr(division, 'time_signature'):
                nonreduced_fraction = mathtools.NonreducedFraction(
                    division.time_signature.pair
                    )
            else:
                nonreduced_fraction = mathtools.NonreducedFraction(division)
            nonreduced_fractions.append(nonreduced_fraction)
        return nonreduced_fractions

    ### PUBLIC PROPERTIES ###

    @property
    def cyclic(self):
        r'''Is true when hypermeasure division maker should treat measure 
        counts cyclically. Otherwise false.

        Set to true or false.
        '''
        return self._cyclic

    @property
    def counts(self):
        r'''Gets measure counts of hypermeasure division maker.

        Set to (possibly empty) list or tuple of positive integers.

        Or set to infinity.
        '''
        return self._counts

    @property
    def secondary_division_maker(self):
        r'''Gets hypermeasure postprocessor of hypermeasure division-maker.

        Returns division-maker or none.
        '''
        return self._secondary_division_maker