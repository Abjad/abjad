# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.rhythmmakertools.DivisionIncisedRhythmMaker \
	import DivisionIncisedRhythmMaker


class DivisionIncisedNoteRhythmMaker(DivisionIncisedRhythmMaker):
    r'''Division-incised note rhythm-maker:

    ..  container:: example

        **Example 1.** Basic usage:

            >>> maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
            ...     prefix_talea=[-1],
            ...     prefix_lengths=[0, 1],
            ...     suffix_talea=[-1],
            ...     suffix_lengths=[1],
            ...     talea_denominator=16)

        Configure at instantiation and then call on any sequence of divisions:

        ::

            >>> divisions = 4 * [(5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

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

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example
    
        **Example 2.** Set `body_ratio` to divide middle part proportionally:

        ::

            >>> maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
            ...     prefix_talea=[-1],
            ...     prefix_lengths=[0, 1],
            ...     suffix_talea=[-1],
            ...     suffix_lengths=[1],
            ...     talea_denominator=16,
            ...     body_ratio=(1, 1))

        ::

            >>> divisions = 4 * [(5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

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

        ::

            >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats division-incised note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=[-1],
                prefix_lengths=[0, 1],
                suffix_talea=[-1],
                suffix_lengths=[1],
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        Returns string.
        '''
        superclass = super(DivisionIncisedNoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Creates new division-incised note rhythm-maker with `kwargs`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=[-1],
                prefix_lengths=[0, 1],
                suffix_talea=[-1],
                suffix_lengths=[1],
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> new_maker = new(maker, prefix_lengths=[1])

        ::

            >>> print format(new_maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=[-1],
                prefix_lengths=[1],
                suffix_talea=[-1],
                suffix_lengths=[1],
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new division-incised note rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            if self.body_ratio is not None:
                shards = mathtools.divide_number_by_ratio(
                    middle, self.body_ratio)
                return tuple(shards)
            else:
                return (middle, )
        else:
            return ()

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses division-incised note rhythm-maker.

        Nonreversed output:

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=[-1],
                prefix_lengths=[0, 1],
                suffix_talea=[-1],
                suffix_lengths=[1],
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Reversed output:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                prefix_talea=[-1],
                prefix_lengths=[1, 0],
                suffix_talea=[-1],
                suffix_lengths=[1],
                talea_denominator=16,
                body_ratio=mathtools.Ratio(1, 1),
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=False,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns division-incised note rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.reverse(self)
