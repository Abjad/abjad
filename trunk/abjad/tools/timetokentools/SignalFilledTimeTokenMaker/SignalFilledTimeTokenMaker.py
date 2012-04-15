from abjad.tools.timetokentools.TokenBurnishedSignalFilledTimeTokenMaker import TokenBurnishedSignalFilledTimeTokenMaker


class SignalFilledTimeTokenMaker(TokenBurnishedSignalFilledTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Signal-affixed time-token maker.

    Configure the time-token maker at initialization::

        abjad> from abjad.tools import sequencetools
        abjad> from abjad.tools import timetokentools

    ::

        abjad> pattern, denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
        abjad> maker = timetokentools.SignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda)

    Then call the time-token maker on arbitrary duration tokens::

        abjad> duration_tokens = [(2, 8), (5, 8)]
        abjad> music = maker(duration_tokens)

    The resulting Abjad objects can be included in any score and the time-token
    make can be called indefinitely on other arbitrary sequences of duration tokens::

        abjad> music = sequencetools.flatten_sequence(music)
        abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
        abjad> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                \times 4/7 {
                    r16
                    c'4
                    r8
                }
            }
            {
                \time 5/8
                \fraction \times 5/7 {
                    c'8.
                    r16
                    c'4
                    r8
                    c'8.
                    r16
                }
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### CLASS ATTRIBUTES ###

    kwargs = (
        'prolation_addenda',
        'secondary_divisions',
        #'pattern_helper',
        #'prolation_addenda_helper',
        #'secondary_divisions_helper',
        )

    ### INITIALIZER ###

    def __init__(self, pattern, denominator, prolation_addenda=None, secondary_divisions=None,
        pattern_helper=None, prolation_addenda_helper=None, secondary_divisions_helper=None):
        lefts, middles, rights = [0], [0], [0]
        left_lengths, right_lengths = [0], [0]
        TokenBurnishedSignalFilledTimeTokenMaker.__init__(self, pattern, denominator, prolation_addenda,
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions,
            pattern_helper=pattern_helper, prolation_addenda_helper=prolation_addenda_helper,
            secondary_divisions_helper=secondary_divisions_helper)
