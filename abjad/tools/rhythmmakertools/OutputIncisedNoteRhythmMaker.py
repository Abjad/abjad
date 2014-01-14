# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.IncisedRhythmMaker \
	import IncisedRhythmMaker


class OutputIncisedNoteRhythmMaker(IncisedRhythmMaker):
    r'''Output-incised note rhythm-maker.

    ::

        >>> maker = rhythmmakertools.IncisedRhythmMaker(
        ...     prefix_talea=(-8, -7),
        ...     prefix_lengths=(2,),
        ...     suffix_talea=(-3,),
        ...     suffix_lengths=(4,),
        ...     talea_denominator=32,
        ...     fill_with_notes=True,
        ...     incise_output=True,
        ...     )

    Configure at initialization and then call on arbitrary divisions:

    ::

        >>> divisions = [(5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = scoretools.make_spacer_skip_measures(divisions)
        >>> staff = scoretools.RhythmicStaff(measures)
        >>> measures = mutate(staff).replace_measure_contents(leaves)
        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _is_output_incised = True

    def __format__(self, format_specification=''):
        r'''Formats output-incised note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(-8, -7),
                prefix_lengths=(2,),
                suffix_talea=(-3,),
                suffix_lengths=(4,),
                talea_denominator=32,
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=False,
                incise_output=True,
                )

        Returns string.
        '''
        superclass = super(IncisedRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new output-incised note rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker, prefix_talea=(-7,))

        ::

            >>> print format(new_maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(-7,),
                prefix_lengths=(2,),
                suffix_talea=(-3,),
                suffix_lengths=(4,),
                talea_denominator=32,
                decrease_durations_monotonically=True,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=False,
                incise_output=True,
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new output-incised note rhythm-maker.
        '''
        return IncisedRhythmMaker.__makenew__(self, *args, **kwargs)

#    ### PRIVATE METHODS ###
#
#    def _make_middle_of_numeric_map_part(self, middle):
#        if 0 < middle:
#            return (middle,)
#        else:
#            return ()

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses output-incised note rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.IncisedRhythmMaker(
                prefix_talea=(-7, -8),
                prefix_lengths=(2,),
                suffix_talea=(-3,),
                suffix_lengths=(4,),
                talea_denominator=32,
                decrease_durations_monotonically=False,
                beam_each_cell=False,
                beam_cells_together=False,
                fill_with_notes=True,
                incise_divisions=False,
                incise_output=True,
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new output-incised note rhythm-maker.
        '''
        return IncisedRhythmMaker.reverse(self)
