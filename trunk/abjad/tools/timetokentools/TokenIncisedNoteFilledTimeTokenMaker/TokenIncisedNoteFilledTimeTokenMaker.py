from abjad.tools.timetokentools.TokenIncisedTimeTokenMaker import TokenIncisedTimeTokenMaker


class TokenIncisedNoteFilledTimeTokenMaker(TokenIncisedTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Token-incised note-filled time-token maker::

        abjad> from abjad.tools import sequencetools
        abjad> from abjad.tools import timetokentools

    ::

        abjad> prefix_signal, prefix_lengths = [-8], [0, 1]
        abjad> suffix_signal, suffix_lengths = [-1], [1]
        abjad> denominator = 32
        abjad> maker = timetokentools.TokenIncisedNoteFilledTimeTokenMaker(prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

    ::

        abjad> duration_tokens = [(5, 8), (5, 8), (5, 8), (5, 8)]
        abjad> leaf_lists = maker(duration_tokens)
        abjad> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
        abjad> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 5/8
                c'2
                c'16.
                r32
            }
            {
                \time 5/8
                r4
                c'4
                c'16.
                r32
            }
            {
                \time 5/8
                c'2
                c'16.
                r32
            }
            {
                \time 5/8
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
