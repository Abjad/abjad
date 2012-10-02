import fractions
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools.timetokentools.TimeTokenMaker import TimeTokenMaker


class TupletMonadTimeTokenMaker(TimeTokenMaker):
    r'''.. versionadded:: 2.10

    Tuplet monad time-token maker::

        >>> maker = timetokentools.TupletMonadTimeTokenMaker()

    ::

        >>> duration_tokens = [(1, 5), (1, 4), (1, 6), (7, 9)]
        >>> tuplet_lists = maker(duration_tokens)
        >>> tuplets = sequencetools.flatten_sequence(tuplet_lists)

    ::

        >>> staff = Staff(tuplets)

    ::

        >>> f(staff)
        \new Staff {
            \times 4/5 {
                c'4
            }
            {
                c'4
            }
            \times 2/3 {
                c'4
            }
            \times 8/9 {
                c'2..
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, duration_tokens, seeds=None):
        result = []
        for duration_token in duration_tokens:
            monad = self._make_monad(duration_token)
            result.append([monad])
        return result

    ### PRIVATE METHODS ###

    def _make_monad(self, duration_token):
        numerator, denominator = duration_token
        binary_denominator = mathtools.greatest_power_of_two_less_equal(denominator)
        duration = fractions.Fraction(abs(numerator), denominator)
        binary_duration = fractions.Fraction(abs(numerator), binary_denominator)
        binary_duration_token = (numerator, binary_denominator) 
        tuplet_multiplier = duration / binary_duration
        leaves = leaftools.make_leaves([0], [binary_duration_token])
        tuplet = tuplettools.Tuplet(tuplet_multiplier, leaves)
        return tuplet
