from abjad.tools.rhythmmakertools.DivisionIncisedRhythmMaker import DivisionIncisedRhythmMaker


class DivisionIncisedNoteRhythmMaker(DivisionIncisedRhythmMaker):
    r'''.. versionadded:: 2.8

    Division-incised note rhythm-maker:

    ::

        >>> prefix_talea, prefix_lengths = [-8], [0, 1]
        >>> suffix_talea, suffix_lengths = [-1], [1]
        >>> talea_denominator = 32
        >>> maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
        ... prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

    ::

        >>> divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> f(staff)
        \new RhythmicStaff {
            {
                \time 5/8
                c'2 ~
                c'16.
                r32
            }
            {
                r4
                c'4 ~
                c'16.
                r32
            }
            {
                c'2 ~
                c'16.
                r32
            }
            {
                r4
                c'4 ~
                c'16.
                r32
            }
        }

    ::
        
        >>> show(staff) # doctest: +SKIP


    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (middle, )
        else:
            return ()

    ### PUBLIC METHODS ###

    def reverse(self):
        '''Reverse division-incised note rhythm-maker.

        Nonreversed output:

        ::

            >>> prefix_talea, prefix_lengths = [-8], [0, 1]
            >>> suffix_talea, suffix_lengths = [-1], [1]
            >>> talea_denominator = 32
            >>> maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker(
            ... prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

        ::

            >>> z(maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                [-8],
                [0, 1],
                [-1],
                [1],
                32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Reversed output:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.DivisionIncisedNoteRhythmMaker(
                [-8],
                [1, 0],
                [-1],
                [1],
                32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=False,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return division-incised note rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.reverse(self)
