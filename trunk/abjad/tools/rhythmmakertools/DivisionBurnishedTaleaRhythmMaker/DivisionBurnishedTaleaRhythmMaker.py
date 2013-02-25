from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.BurnishedRhythmMaker import BurnishedRhythmMaker


class DivisionBurnishedTaleaRhythmMaker(BurnishedRhythmMaker):
    r'''.. versionadded:: 2.8

    Division-burnished talea rhythm-maker:

    ::

        >>> maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        ...     talea=[1, 1, 2, 4],
        ...     talea_denominator=16,
        ...     prolation_addenda=[0, 3],
        ...     lefts=[-1],
        ...     middles=[0],
        ...     rights=[-1],
        ...     left_lengths=[1],
        ...     right_lengths=[1],
        ...     secondary_divisions=[14])

    Configure at instantiation and then call on any sequence of divisions:

    ::

        >>> divisions = [(5, 8), (5, 8)]
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
        lefts, middles, rights, left_lengths, right_lengths=quintuplet
        lefts_index, rights_index = 0, 0
        burnished_divisions = []
        for division_index, division in enumerate(divisions):
            left_length = left_lengths[division_index]
            left = lefts[lefts_index:lefts_index+left_length]
            lefts_index += left_length
            right_length = right_lengths[division_index]
            right = rights[rights_index:rights_index+right_length]
            rights_index += right_length
            available_left_length = len(division)
            left_length = min([left_length, available_left_length])
            available_right_length = len(division) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(division) - left_length - right_length

            left = left[:left_length]
            middle = middle_length * [middles[division_index]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                division, [left_length, middle_length, right_length], cyclic=False, overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def storage_format(self):
        '''Division-burnished talea rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=[1, 1, 2, 4],
                talea_denominator=16,
                prolation_addenda=[0, 3],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[14],
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                tie_rests=False
                )

        Return string.
        '''
        return BurnishedTaleaRhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new rhythm-maker with `kwargs`:

        ::

            >>> z(maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=[1, 1, 2, 4],
                talea_denominator=16,
                prolation_addenda=[0, 3],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[14],
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                tie_rests=False
                )

        ::

            >>> new_maker = maker.new(talea=[1, 1, 2])

        ::

            >>> z(new_maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=[1, 1, 2],
                talea_denominator=16,
                prolation_addenda=[0, 3],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[14],
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new division-burnished talea rhythm-maker.
        '''
        return BurnishedRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse division-burnished talea rhythm-maker.

        Nonreversed output:

        ::

            >>> z(maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=[1, 1, 2, 4],
                talea_denominator=16,
                prolation_addenda=[0, 3],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[14],
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Reversed output:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=[4, 2, 1, 1],
                talea_denominator=16,
                prolation_addenda=[3, 0],
                lefts=[-1],
                middles=[0],
                rights=[-1],
                left_lengths=[1],
                right_lengths=[1],
                secondary_divisions=[14],
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=False,
                tie_split_notes=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new division-burnished talea rhythm-maker.
        '''
        return BurnishedRhythmMaker.reverse(self)
