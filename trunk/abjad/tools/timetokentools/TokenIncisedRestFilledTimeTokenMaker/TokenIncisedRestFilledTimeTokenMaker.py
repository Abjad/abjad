from abjad.tools.timetokentools.TokenIncisedTimeTokenMaker import TokenIncisedTimeTokenMaker


class TokenIncisedRestFilledTimeTokenMaker(TokenIncisedTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Token-incised rest-filled time-token maker::

        abjad> from abjad.tools import sequencetools
        abjad> from abjad.tools import timetokentools

    ::

        abjad> prefix_signal, prefix_lengths = [8], [1, 2, 3, 4]
        abjad> suffix_signal, suffix_lengths = [1], [1]
        abjad> denominator = 32
        abjad> maker = timetokentools.TokenIncisedRestFilledTimeTokenMaker(prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

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
                c'4
                r4
                r16.
                c'32
            }
            {
                \time 5/8
                c'4
                c'4
                r16.
                c'32
            }
            {
                \time 5/8
                c'4
                c'4
                c'8
            }
            {
                \time 5/8
                c'4
                c'4
                c'8
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()
