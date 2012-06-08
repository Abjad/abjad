from abjad.tools.timetokentools.TokenIncisedRestFilledTimeTokenMaker import TokenIncisedRestFilledTimeTokenMaker


class RestFilledTimeTokenMaker(TokenIncisedRestFilledTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Rest-filled time-token maker::

        >>> from abjad.tools import sequencetools
        >>> from abjad.tools import timetokentools

    ::

        >>> maker = timetokentools.RestFilledTimeTokenMaker()

    ::

        >>> duration_tokens = [(5, 16), (3, 8)]
        >>> leaf_lists = maker(duration_tokens)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        >>> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
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

    Return time-token maker.
    '''

    ### INITIALIZER ###

    def __init__(self):
        TokenIncisedRestFilledTimeTokenMaker.__init__(self, [], [0], [], [0], 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
