from abjad.tools.timetokentools.TokenIncisedRestFilledTimeTokenMaker import TokenIncisedRestFilledTimeTokenMaker


class RestFilledTimeTokenMaker(TokenIncisedRestFilledTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Rest-filled time-token maker::

        abjad> from abjad.tools import sequencetools
        abjad> from abjad.tools import timetokentools

    ::

        abjad> maker = timetokentools.RestFilledTimeTokenMaker()

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
                r4
                r16
            }
            {
                \time 3/8
                r4.
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### CLASS ATTRIBUTES ###

    args = ()
    kwargs = ()

    ### INITIALIZER ###

    def __init__(self):
        TokenIncisedRestFilledTimeTokenMaker.__init__(self, [], [0], [], [0], 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
