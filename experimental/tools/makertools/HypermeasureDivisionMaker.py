# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class HypermeasureDivisionMaker(AbjadValueObject):
    r'''Hypermeasure division-maker.

    ..  container:: example

        **Example 1.** Groups measures together two at a time:

        ::

            >>> division_maker = makertools.HypermeasureDivisionMaker(
            ...     measure_counts=[2],
            ...     )

        ::

            >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(4, 8)]
            [Division(8, 8)]
            [Division(2, 4)]

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
                c'2
                c'1
                c'2
            }

    ..  container:: example

        **Example 2.** Groups measures together two at a time and fills
        resulting hypemeasure divisions with ``3/16`` divisions:

        ::

            >>> divisions = makertools.SplitDivisionMaker(
            ...     durations=[Duration(3, 16)],
            ...     remainder=Right,
            ...     )
            >>> division_maker = makertools.HypermeasureDivisionMaker(
            ...     measure_counts=[2],
            ...     secondary_division_maker=divisions,
            ...     )

        ::

            >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            [Division(3, 16), Division(3, 16), Division(1, 8)]
            [Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(1, 16)]
            [Division(3, 16), Division(3, 16), Division(1, 8)]


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
        '_measure_counts',
        '_secondary_division_maker',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=True,
        measure_counts=None,
        secondary_division_maker=None,
        ):
        from experimental import makertools
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        measure_counts = measure_counts or ()
        if measure_counts == mathtools.Infinity:
            self._measure_counts = measure_counts
        else:
            assert mathtools.all_are_positive_integers(measure_counts)
            self._measure_counts = measure_counts
        if secondary_division_maker is not None:
            prototype = (makertools.SplitDivisionMaker,)
            assert isinstance(secondary_division_maker, prototype)
        self._secondary_division_maker = secondary_division_maker

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls hypermeasure division-maker.

        ..  container:: example

            **Example 1.** Returns measures ungrouped:

            ::

                >>> division_maker = makertools.HypermeasureDivisionMaker()

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(2, 8)]
                [Division(2, 8)]
                [Division(4, 8)]
                [Division(4, 8)]
                [Division(2, 4)]

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

            **Example 2.** Groups measures together two at a time:

            ::

                >>> division_maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=None,
                ...     )

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(4, 8)]
                [Division(8, 8)]
                [Division(2, 4)]

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
                    c'1
                    c'2
                }

        ..  container:: example

            **Example 3a.** Groups measures together two at a time and fills
            resulting hypermeasure divisions with ``3/16`` divisions.

            Remainders to the right:
            
            ::

                >>> divisions = makertools.SplitDivisionMaker(
                ...     durations=[(3, 16)],
                ...     remainder=Right,
                ...     )
                >>> division_maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=divisions,
                ...     )

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(3, 16), Division(3, 16), Division(1, 8)]
                [Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(1, 16)]
                [Division(3, 16), Division(3, 16), Division(1, 8)]

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

                >>> divisions = makertools.SplitDivisionMaker(
                ...     durations=[(3, 16)],
                ...     remainder=Left,
                ...     )
                >>> division_maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=divisions,
                ...     )

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 8), Division(3, 16), Division(3, 16)]
                [Division(1, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16)]
                [Division(1, 8), Division(3, 16), Division(3, 16)]

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

            **Example 4.** Groups all measures together:

            ::

                >>> division_maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=mathtools.Infinity,
                ...     )

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(16, 8)]

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
                    c'\breve
                }

        ..  container:: example

            **Example 5a.** Glues all input divisions together and then divides
            into divisions of ``3/8``. 

            Remainder at right:

            ::

                >>> divisions = makertools.SplitDivisionMaker(
                ...     durations=[(3, 16)],
                ...     remainder=Right,
                ...     )
                >>> division_maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=mathtools.Infinity,
                ...     secondary_division_maker=divisions,
                ...     )

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(1, 8)]

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

                >>> divisions = makertools.SplitDivisionMaker(
                ...     durations=[(3, 16)],
                ...     remainder=Left,
                ...     )
                >>> division_maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=mathtools.Infinity,
                ...     secondary_division_maker=divisions,
                ...     )

            ::

                >>> time_signatures = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division(1, 8), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16), Division(3, 16)]

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

                >>> time_signatures = []
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list

        Returns list of division lists.
        '''
        divisions = divisions or ()
        divisions = self._coerce_divisions(divisions)
        if not divisions:
            pass
        elif self.measure_counts == mathtools.Infinity:
            divisions = [sum(divisions)]
        elif self.measure_counts:
            parts = sequencetools.partition_sequence_by_counts(
                divisions,
                self.measure_counts,
                cyclic=self.cyclic,
                overhang=True,
                )
            divisions = [sum(_) for _ in parts]
        division_lists = []
        for division in divisions:
            if self.secondary_division_maker is not None:
                division_list = self.secondary_division_maker([division])[0]
            else:
                division_list = [division]
            division_list = [durationtools.Division(_) for _ in division_list]
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
        if not self.measure_counts:
            keyword_argument_names.remove('measure_counts')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PRIVATE METHODS ###

    def _coerce_divisions(self, divisions):
        nonreduced_fractions = []
        for division in divisions:
            if hasattr(division, 'time_signature'):
                nonreduced_fraction = durationtools.Division(
                    division.time_signature.pair
                    )
            else:
                nonreduced_fraction = durationtools.Division(division)
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
    def measure_counts(self):
        r'''Gets measure counts of hypermeasure division maker.

        Set to (possibly empty) list or tuple of positive integers.

        Or set to infinity.
        '''
        return self._measure_counts

    @property
    def secondary_division_maker(self):
        r'''Gets hypermeasure postprocessor of hypermeasure division-maker.

        Returns division-maker or none.
        '''
        return self._secondary_division_maker