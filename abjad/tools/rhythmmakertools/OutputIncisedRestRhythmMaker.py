# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.OutputIncisedRhythmMaker \
	import OutputIncisedRhythmMaker


class OutputIncisedRestRhythmMaker(OutputIncisedRhythmMaker):
    r'''Output-incised rest rhythm-maker:

    ::

        >>> maker = rhythmmakertools.OutputIncisedRestRhythmMaker(
        ...     prefix_talea=[7, 8],
        ...     prefix_lengths=[2],
        ...     suffix_talea=[3],
        ...     suffix_lengths=[4],
        ...     talea_denominator=32)

    Configuration at initialization and then call on arbitrary divisions:

    ::

        >>> divisions = [(5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = \
        ...     scoretools.make_measures_with_full_measure_spacer_skips(
        ...     divisions)
        >>> staff = scoretools.RhythmicStaff(measures)
        >>> measures = scoretools.replace_contents_of_measures_in_expr(
        ...     staff, leaves)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()

    ### PUBLIC PROPERTES ###

    @property
    def storage_format(self):
        r'''Output-incised rest rhythm-maker storage format:

        ::

            >>> print maker.storage_format
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
                beam_cells_together=False
                )

        Returns string.
        '''
        return OutputIncisedRhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        r'''Create new output-incised rest rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new(prefix_talea=[7])

        ::

            >>> print new_maker.storage_format
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
                beam_cells_together=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new output-incised rest rhythm-maker.
        '''
        return OutputIncisedRhythmMaker.new(self, **kwargs)

    def reverse(self):
        r'''Reverse output-incised rest rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print reversed_maker.storage_format
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
                beam_cells_together=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new output-incised rest rhythm-maker.
        '''
        return OutputIncisedRhythmMaker.reverse(self)
