from abjad.tools.rhythmmakertools.OutputIncisedRhythmMaker import OutputIncisedRhythmMaker


class OutputIncisedNoteRhythmMaker(OutputIncisedRhythmMaker):
    r'''.. versionadded:: 2.8

    Output-incised note rhythm-maker:

    ::

        >>> maker = rhythmmakertools.OutputIncisedNoteRhythmMaker(
        ...     prefix_talea=[-8, -7],
        ...     prefix_lengths=[2],
        ...     suffix_talea=[-3],
        ...     suffix_lengths=[4],
        ...     talea_denominator=32)

    Configure at initialization and then call on arbitrary divisions:

    ::

        >>> divisions = [(5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (middle, )
        else:
            return ()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Output-incised note rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.OutputIncisedNoteRhythmMaker(
                prefix_talea=[-8, -7],
                prefix_lengths=[2],
                suffix_talea=[-3],
                suffix_lengths=[4],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        Return string.
        '''
        return OutputIncisedRhythmMaker.storage_format(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new output-incised note rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new(prefix_talea=[-7])

        ::

            >>> z(new_maker)
            rhythmmakertools.OutputIncisedNoteRhythmMaker(
                prefix_talea=[-7],
                prefix_lengths=[2],
                suffix_talea=[-3],
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
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new output-incised note rhythm-maker.
        '''
        return OutputIncisedRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse output-incised note rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.OutputIncisedNoteRhythmMaker(
                prefix_talea=[-7, -8],
                prefix_lengths=[2],
                suffix_talea=[-3],
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
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new output-incised note rhythm-maker.
        '''
        return OutputIncisedRhythmMaker.reverse(self)
