from abjad.tools.rhythmmakertools.DivisionIncisedRhythmMaker import DivisionIncisedRhythmMaker


class DivisionIncisedRestFilledRhythmMaker(DivisionIncisedRhythmMaker):
    r'''.. versionadded:: 2.8

    Division-incised rest-filled rhythm-maker::

        >>> prefix_talea, prefix_lengths = [8], [1, 2, 3, 4]
        >>> suffix_talea, suffix_lengths = [1], [1]
        >>> talea_denominator = 32
        >>> maker = rhythmmakertools.DivisionIncisedRestFilledRhythmMaker(
        ... prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

    ::

        >>> divisions = [(5, 8), (5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> f(staff) 
        \new Staff {
            {
                \time 5/8
                c'4
                r4
                r16.
                c'32
            }
            {
                c'4
                c'4
                r16.
                c'32
            }
            {
                c'4
                c'4
                c'8
            }
            {
                c'4
                c'4
                c'8
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()
