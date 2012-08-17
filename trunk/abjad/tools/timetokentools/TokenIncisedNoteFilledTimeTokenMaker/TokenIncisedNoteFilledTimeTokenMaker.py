from abjad.tools.timetokentools.TokenIncisedTimeTokenMaker import TokenIncisedTimeTokenMaker


class TokenIncisedNoteFilledTimeTokenMaker(TokenIncisedTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Token-incised note-filled time-token maker::

        >>> from abjad.tools import sequencetools
        >>> from abjad.tools import timetokentools

    ::

        >>> prefix_signal, prefix_lengths = [-8], [0, 1]
        >>> suffix_signal, suffix_lengths = [-1], [1]
        >>> denominator = 32
        >>> maker = timetokentools.TokenIncisedNoteFilledTimeTokenMaker(
        ... prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

    ::

        >>> duration_tokens = [(5, 8), (5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(duration_tokens)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 5/8
                c'2
                c'16.
                r32
            }
            {
                r4
                c'4
                c'16.
                r32
            }
            {
                c'2
                c'16.
                r32
            }
            {
                r4
                c'4
                c'16.
                r32
            }
        }


    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (middle, )
        else:
            return ()
