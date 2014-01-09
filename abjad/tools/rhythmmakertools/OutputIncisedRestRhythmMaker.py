# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.OutputIncisedRhythmMaker \
	import OutputIncisedRhythmMaker


class OutputIncisedRestRhythmMaker(OutputIncisedRhythmMaker):
    r'''Output-incised rest rhythm-maker.

    ::

        >>> maker = rhythmmakertools.OutputIncisedRestRhythmMaker(
        ...     prefix_talea=[7, 8],
        ...     prefix_lengths=[2],
        ...     suffix_talea=[3],
        ...     suffix_lengths=[4],
        ...     talea_denominator=32,
        ...     )

    Configuration at initialization and then call on arbitrary divisions:

    ::

        >>> divisions = [(5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = scoretools.make_spacer_skip_measures(divisions)
        >>> staff = scoretools.RhythmicStaff(measures)
        >>> measures = scoretools.replace_contents_of_measures_in_expr(
        ...     staff, leaves)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats output-incised rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.OutputIncisedRestRhythmMaker(
                prefix_talea=[7, 8],
                prefix_lengths=[2],
                suffix_talea=[3],
                suffix_lengths=[4],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        Returns string.
        '''
        superclass = super(OutputIncisedRestRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new output-incised rest rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker, prefix_talea=[7])

        ::

            >>> print format(new_maker)
            rhythmmakertools.OutputIncisedRestRhythmMaker(
                prefix_talea=[7],
                prefix_lengths=[2],
                suffix_talea=[3],
                suffix_lengths=[4],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new output-incised rest rhythm-maker.
        '''
        return OutputIncisedRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses output-incised rest rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.OutputIncisedRestRhythmMaker(
                prefix_talea=[8, 7],
                prefix_lengths=[2],
                suffix_talea=[3],
                suffix_lengths=[4],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=False,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new output-incised rest rhythm-maker.
        '''
        return OutputIncisedRhythmMaker.reverse(self)
