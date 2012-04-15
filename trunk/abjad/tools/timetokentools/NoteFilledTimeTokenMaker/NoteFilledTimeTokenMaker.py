from abjad.tools.timetokentools.TokenIncisedNoteFilledTimeTokenMaker import TokenIncisedNoteFilledTimeTokenMaker


class NoteFilledTimeTokenMaker(TokenIncisedNoteFilledTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Note-filled time-token maker::

        abjad> from abjad.tools import sequencetools
        abjad> from abjad.tools import timetokentools
    
    ::

        abjad> maker = timetokentools.NoteFilledTimeTokenMaker()

    ::

        abjad> duration_tokens = [(5, 16), (3, 8)]
        abjad> leaf_lists = maker(duration_tokens)
        abjad> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
        abjad> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 5/16
                c'4
                c'16
            }
            {
                \time 3/8
                c'4.
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### CLASS ATTRIBUTES ###

    args = ()
    kwargs = ()

    def __init__(self):
        TokenIncisedNoteFilledTimeTokenMaker.__init__(self, [], [0], [], [0], 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
