import fractions
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class TupletMonadRhythmMaker(RhythmMaker):
    r'''.. versionadded:: 2.10

    Tuplet monad rhythm-maker::

        >>> maker = rhythmmakertools.TupletMonadRhythmMaker()

    ::

        >>> divisions = [(1, 5), (1, 4), (1, 6), (7, 9)]
        >>> tuplet_lists = maker(divisions)
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

    Return rhythm-maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, beam_each_cell=False, beam_cells_together=False):
        RhythmMaker.__init__(self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together
            )

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        result = []
        for division in divisions:
            monad = self._make_monad(division)
            result.append([monad])
        return result

    ### PRIVATE METHODS ###

    def _make_monad(self, division):
        numerator, talea_denominator = division
        power_of_two_denominator = mathtools.greatest_power_of_two_less_equal(talea_denominator)
        duration = fractions.Fraction(abs(numerator), talea_denominator)
        power_of_two_duration = fractions.Fraction(abs(numerator), power_of_two_denominator)
        power_of_two_division = (numerator, power_of_two_denominator) 
        tuplet_multiplier = duration / power_of_two_duration
        leaves = leaftools.make_leaves([0], [power_of_two_division])
        tuplet = tuplettools.Tuplet(tuplet_multiplier, leaves)
        return tuplet
