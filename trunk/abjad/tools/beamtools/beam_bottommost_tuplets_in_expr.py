from abjad.tools import componenttools
from abjad.tools import tuplettools


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

        abjad> beamtools.beam_bottommost_tuplets_in_expr(staff)

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

    .. versionchanged:: 2.9
        renamed ``tuplettools.beam_bottommost_tuplets_in_expr()`` to
        ``beamtools.beam_bottommost_tuplets_in_expr()``.
    '''
    from abjad.tools import beamtools

    for tuplet in componenttools.iterate_components_forward_in_expr(expr, tuplettools.Tuplet):
        for component in tuplet:
            if isinstance(component, tuplettools.Tuplet):
                break
        else:
            beamtools.MultipartBeamSpanner(tuplet)
