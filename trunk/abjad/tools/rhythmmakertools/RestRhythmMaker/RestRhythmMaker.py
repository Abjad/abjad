from abjad.tools.rhythmmakertools.DivisionIncisedRestRhythmMaker import DivisionIncisedRestRhythmMaker


class RestRhythmMaker(DivisionIncisedRestRhythmMaker):
    r'''.. versionadded:: 2.8

    Rest rhythm-maker::

        >>> maker = rhythmmakertools.RestRhythmMaker()

    ::

        >>> divisions = [(5, 16), (3, 8)]
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
                \time 5/16
                r4
                r16
            }
            {
                \time 3/8
                r4.
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self):
        DivisionIncisedRestRhythmMaker.__init__(
            self, [], [0], [], [0], 1,
            decrease_durations_monotonically=True, tie_rests=False
            )
