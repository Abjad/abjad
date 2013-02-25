from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.BurnishedRhythmMaker import BurnishedRhythmMaker


class OutputBurnishedTaleaRhythmMaker(BurnishedRhythmMaker):
    r'''.. versionadded:: 2.8

    Output-burnished talea rhythm-maker:

    ::

        >>> maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        ...     talea=[1, 2, 3],
        ...     talea_denominator=16,
        ...     prolation_addenda=[0, 2],
        ...     lefts=[-1],
        ...     middles=[0],
        ...     rights=[-1],
        ...     left_lengths=[1],
        ...     right_lengths=[1],
        ...     secondary_divisions=[9],
        ...     beam_each_cell=True)

    Configure at initialization and then call on any list of divisions:

    ::

        >>> divisions = [(3, 8), (4, 8)]
        >>> music = maker(divisions)
        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### PRIVATE METHODS ###

    def _burnish_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        burnished_divisions = []
        left_length = left_lengths[0]
        left = lefts[:left_length]
        right_length = right_lengths[0]
        right = rights[:right_length]
        if len(divisions) == 1:
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            available_right_length = len(divisions[0]) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[0]) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[0], [left_length, middle_length, right_length], cyclic=False, overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        else:
            ## first division
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            middle_length = len(divisions[0]) - left_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            left_part, middle_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[0], [left_length, middle_length], cyclic=False, overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            burnished_division = left_part + middle_part
            burnished_divisions.append(burnished_division)
            ## middle divisions
            for division in divisions[1:-1]:
                middle_part = division
                middle = len(division) * [middles[0]]
                middle_part = self._burnish_division_part(middle_part, middle)
                burnished_division = middle_part
                burnished_divisions.append(burnished_division)
            ## last division:
            available_right_length = len(divisions[-1])
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[-1]) - right_length
            right = right[:right_length]
            middle = middle_length * [middles[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[-1], [middle_length, right_length], cyclic=False, overhang=False)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Output-burnished talea rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
                talea=[1, 2, 3],
                talea_denominator=16,
                prolation_addenda=[0, 2],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[9],
                beam_each_cell=True,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                tie_rests=False
                )

        Return string.
        '''
        return BurnishedRhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new output-burnished talea rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new(secondary_divisions=[10])

        ::

            >>> z(new_maker)
            rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
                talea=[1, 2, 3],
                talea_denominator=16,
                prolation_addenda=[0, 2],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[10],
                beam_each_cell=True,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(3, 8), (4, 8)]
            >>> music = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new output-burnished talea rhythm-maker.
        '''
        return BurnishedRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse output-burnished talea rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
                talea=[3, 2, 1],
                talea_denominator=16,
                prolation_addenda=[2, 0],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[9],
                beam_each_cell=True,
                beam_cells_together=False,
                decrease_durations_monotonically=False,
                tie_split_notes=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(3, 8), (4, 8)]
            >>> music = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new output-burnished talea rhythm-maker.
        '''
        return BurnishedRhythmMaker.reverse(self)
