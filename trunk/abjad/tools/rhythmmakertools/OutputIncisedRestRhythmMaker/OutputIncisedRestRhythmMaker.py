from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.OutputIncisedRhythmMaker import OutputIncisedRhythmMaker


class OutputIncisedRestRhythmMaker(OutputIncisedRhythmMaker):
    r'''.. versionadded:: 2.8

    Output-incised rest-filled rhythm-maker.

    Configure the rhythm-maker on initialization::

        >>> prefix_talea, prefix_lengths = [8], [2]
        >>> suffix_talea, suffix_lengths = [3], [4]
        >>> talea_denominator = 32
        >>> maker = rhythmmakertools.OutputIncisedRestRhythmMaker(
        ... prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator)

    Then call the rhythm-maker on arbitrary divisions::

        >>> divisions = [(5, 8), (5, 8), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    The resulting Abjad objects can be included in any score and the rhythm 
    maker can be reused::

        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
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

    Return rhythm-maker.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()
