from abjad.tools import iterationtools
from abjad.tools import tuplettools


def apply_multipart_beam_spanner_to_bottommost_tuplets_in_expr(expr):
    r'''Beam bottommost tuplets in `expr`::

        >>> staff = Staff(3 * Tuplet(Fraction(2, 3), "c'8 d'8 e'8"))

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

        >>> beamtools.apply_multipart_beam_spanner_to_bottommost_tuplets_in_expr(staff)

    ::

        >>> f(staff)
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
        ``beamtools.apply_multipart_beam_spanner_to_bottommost_tuplets_in_expr()``.

    .. versionchanged:: 2.9
        renamed ``beamtools.beam_bottommost_tuplets_in_expr()`` to
        ``beamtools.apply_multipart_beam_spanner_to_bottommost_tuplets_in_expr()``.
    '''
    from abjad.tools import beamtools

    for tuplet in iterationtools.iterate_components_in_expr(expr, tuplettools.Tuplet):
        for component in tuplet:
            if isinstance(component, tuplettools.Tuplet):
                break
        else:
            beamtools.MultipartBeamSpanner(tuplet)
