# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.IncisedRhythmMaker import IncisedRhythmMaker


class DivisionIncisedNoteRhythmMaker(IncisedRhythmMaker):
    r'''Division-incised note rhythm-maker.

    ..  container:: example

        Basic usage:

        ::

            >>> maker = rhythmmakertools.IncisedRhythmMaker(
            ...     prefix_talea=(-1,),
            ...     prefix_lengths=(0, 1),
            ...     suffix_talea=(-1,),
            ...     suffix_lengths=(1,),
            ...     talea_denominator=16,
            ...     fill_with_notes=True,
            ...     incise_divisions=True,
            ...     )

        Configure at instantiation and then call on any sequence of divisions:

        ::

            >>> divisions = 4 * [(5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new RhythmicStaff {
                {
                    \time 5/16
                    c'4
                    r16
                }
                {
                    r16
                    c'8.
                    r16
                }
                {
                    c'4
                    r16
                }
                {
                    r16
                    c'8.
                    r16
                }
            }

    ..  container:: example
    
        Sets `body_ratio` to divide middle part proportionally:

        ::

            >>> maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
            ...     prefix_talea=(-1,),
            ...     prefix_lengths=(0, 1),
            ...     suffix_talea=(-1,),
            ...     suffix_lengths=(1,),
            ...     talea_denominator=16,
            ...     body_ratio=(1, 1),
            ...     fill_with_notes=True,
            ...     incise_divisions=True,
            ...     )

        ::

            >>> divisions = 4 * [(5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new RhythmicStaff {
                {
                    \time 5/16
                    c'8
                    c'8
                    r16
                }
                {
                    r16
                    c'16.
                    c'16.
                    r16
                }
                {
                    c'8
                    c'8
                    r16
                }
                {
                    r16
                    c'16.
                    c'16.
                    r16
                }
            }

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _fill_class = scoretools.Note

    _is_division_incised = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats division-incised note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=(-1,),
                prefix_lengths=(0, 1),
                suffix_talea=(-1,),
                suffix_lengths=(1,),
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=True,
                incise_output=False,
                )

        Returns string.
        '''
        superclass = super(DivisionIncisedNoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new division-incised note rhythm-maker with `kwargs`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=(-1,),
                prefix_lengths=(0, 1),
                suffix_talea=(-1,),
                suffix_lengths=(1,),
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> new_maker = new(maker, prefix_lengths=(1,))

        ::

            >>> print format(new_maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=(-1,),
                prefix_lengths=(1,),
                suffix_talea=(-1,),
                suffix_lengths=(1,),
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new division-incised note rhythm-maker.
        '''
        return IncisedRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses division-incised note rhythm-maker.

        Nonreversed output:

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=(-1,),
                prefix_lengths=(0, 1),
                suffix_talea=(-1,),
                suffix_lengths=(1,),
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Reversed output:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=(-1,),
                prefix_lengths=(1, 0),
                suffix_talea=(-1,),
                suffix_lengths=(1,),
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                decrease_durations_monotonically=False,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns division-incised note rhythm-maker.
        '''
        return IncisedRhythmMaker.reverse(self)
