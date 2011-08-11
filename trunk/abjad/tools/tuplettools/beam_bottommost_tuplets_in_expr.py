#from abjad.tools.spannertools import BeamSpanner
from abjad.tools.spannertools import MultipartBeamSpanner
from abjad.tools import componenttools
from abjad.tools.tuplettools.Tuplet import Tuplet


def beam_bottommost_tuplets_in_expr(expr):
    r'''Beam bottommost tuplets in `expr`::

        abjad> staff = Staff(3 * Tuplet(Fraction(2, 3), "c'8 d'8 e'8"))

    ::

        f(staff)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
        }

    ::

        abjad> tuplettools.beam_bottommost_tuplets_in_expr(staff)

    ::

        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
        }

    Return none.
    '''

    for tuplet in componenttools.iterate_components_forward_in_expr(expr, Tuplet):
        for component in tuplet:
            if isinstance(component, Tuplet):
                break
        else:
            MultipartBeamSpanner(tuplet)
