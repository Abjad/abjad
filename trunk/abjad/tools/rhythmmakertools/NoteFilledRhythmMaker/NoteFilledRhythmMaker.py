from abjad.tools.rhythmmakertools.DivisionIncisedNoteFilledRhythmMaker import DivisionIncisedNoteFilledRhythmMaker


class NoteFilledRhythmMaker(DivisionIncisedNoteFilledRhythmMaker):
    r'''.. versionadded:: 2.8

    Note-filled rhythm-maker::

        >>> maker = rhythmmakertools.NoteFilledRhythmMaker()

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

    _default_mandatory_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, big_endian=True, tie_rests=False):
        DivisionIncisedNoteFilledRhythmMaker.__init__(
            self, [], [0], [], [0], 1,
            big_endian=big_endian, tie_rests=tie_rests
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
