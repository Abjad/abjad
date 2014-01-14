# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.IncisedRhythmMaker import IncisedRhythmMaker


class DivisionIncisedRestRhythmMaker(IncisedRhythmMaker):
    r'''Division-incised rest rhythm-maker.

    ..  container:: example

        Basic usage:

        ::

            >>> maker = rhythmmakertools.IncisedRhythmMaker(
            ...     prefix_talea=(1,),
            ...     prefix_lengths=(1, 2, 3, 4),
            ...     suffix_talea=(1,),
            ...     suffix_lengths=(1,),
            ...     talea_denominator=32,
            ...     fill_with_notes=False,
            ...     incise_divisions=True,
            ...     )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _fill_class = scoretools.Rest

    _is_division_incised = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats division-incised rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(1,),
                prefix_lengths=(1, 2, 3, 4),
                suffix_talea=(1,),
                suffix_lengths=(1,),
                talea_denominator=32,
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=False,
                incise_divisions=True,
                incise_output=False,
                )

        Returns string.
        '''
        superclass = super(IncisedRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new division-incised rest rhythm-maker with `kwargs`.

        ::

            >>> print format(maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(1,),
                prefix_lengths=(1, 2, 3, 4),
                suffix_talea=(1,),
                suffix_lengths=(1,),
                talea_denominator=32,
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=False,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> new_maker = new(maker, suffix_lengths=(0,))

        ::

            >>> print format(new_maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(1,),
                prefix_lengths=(1, 2, 3, 4),
                suffix_talea=(1,),
                suffix_lengths=(0,),
                talea_denominator=32,
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=False,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new division-incised rest rhythm-maker.
        '''
        return IncisedRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses division-incised rest rhythm-maker.

        ::

            >>> print format(maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(1,),
                prefix_lengths=(1, 2, 3, 4),
                suffix_talea=(1,),
                suffix_lengths=(1,),
                talea_denominator=32,
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=False,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(1,),
                prefix_lengths=(4, 3, 2, 1),
                suffix_talea=(1,),
                suffix_lengths=(1,),
                talea_denominator=32,
                decrease_durations_monotonically=False,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=False,
                incise_divisions=True,
                incise_output=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new division-incised rest rhythm-maker.
        '''
        return IncisedRhythmMaker.reverse(self)
