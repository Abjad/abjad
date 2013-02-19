from abjad.tools.rhythmmakertools.DivisionIncisedRhythmMaker import DivisionIncisedRhythmMaker


class DivisionIncisedRestRhythmMaker(DivisionIncisedRhythmMaker):
    r'''.. versionadded:: 2.8

    Division-incised rest rhythm-maker:

    ::

        >>> maker = rhythmmakertools.DivisionIncisedRestRhythmMaker(
        ...     prefix_talea=[1],
        ...     prefix_lengths=[1, 2, 3, 4],
        ...     suffix_talea=[1],
        ...     suffix_lengths=[1],
        ...     talea_denominator=32)

    Configure at instantiation and then call on any sequence of divisions:

    ::

        >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

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

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def storage_format(self):
        '''Division-incised rest rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[1],
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
        return DivisionIncisedRhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new division-incised rest rhythm-maker with `kwargs`:
    
        ::

            >>> z(maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        ::

            >>> new_maker = maker.new(suffix_lengths=[0])

        ::

            >>> z(new_maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[0],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new division-incised rest rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse division-incised rest rhythm-maker:

        ::

            >>> z(maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[4, 3, 2, 1],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=False,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new division-incised rest rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.reverse(self)
