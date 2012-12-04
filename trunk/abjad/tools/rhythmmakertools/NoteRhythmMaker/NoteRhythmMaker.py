from abjad.tools.rhythmmakertools.DivisionIncisedNoteRhythmMaker import DivisionIncisedNoteRhythmMaker


class NoteRhythmMaker(DivisionIncisedNoteRhythmMaker):
    r'''.. versionadded:: 2.8

    Note rhythm-maker::

        >>> maker = rhythmmakertools.NoteRhythmMaker()

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
                c'4 ~
                c'16
            }
            {
                \time 3/8
                c'4.
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, decrease_durations_monotonically=True, tie_rests=False):
        DivisionIncisedNoteRhythmMaker.__init__(
            self, [], [0], [], [0], 1,
            decrease_durations_monotonically=decrease_durations_monotonically, tie_rests=tie_rests
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
