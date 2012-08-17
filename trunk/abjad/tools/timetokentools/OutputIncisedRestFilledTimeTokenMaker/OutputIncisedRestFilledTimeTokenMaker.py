from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.timetokentools.OutputIncisedTimeTokenMaker import OutputIncisedTimeTokenMaker


class OutputIncisedRestFilledTimeTokenMaker(OutputIncisedTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Output-incised rest-filled time-token maker.

    Configure the time-token maker on initialization::

        >>> from abjad.tools import sequencetools
        >>> from abjad.tools import timetokentools

    ::

        >>> prefix_signal, prefix_lengths = [8], [2]
        >>> suffix_signal, suffix_lengths = [3], [4]
        >>> denominator = 32
        >>> maker = timetokentools.OutputIncisedRestFilledTimeTokenMaker(
        ... prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator)

    Then call the time-token maker on arbitrary duration tokens::

        >>> duration_tokens = [(5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(duration_tokens)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    The resulting Abjad objects can be included in any score and the time-token 
    maker can be reused::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 5/8
                c'4
                c'4
                r8
            }
            {
                r2
                r8
            }
            {
                r4
                c'16.
                c'16.
                c'16.
                c'16.
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
