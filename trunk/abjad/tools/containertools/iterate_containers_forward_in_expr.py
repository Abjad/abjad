from abjad.tools.containertools.Container import Container
from abjad.tools import componenttools


def iterate_containers_forward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate containers forward in `expr`::

        abjad> staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
        abjad> Tuplet(Fraction(2, 3), staff[1][:])
        Tuplet(2/3, [e'8, f'8, g'8])
        abjad> staff.is_parallel = True

    ::

        abjad> f(staff)
        \new Staff <<
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                \times 2/3 {
                    e'8
                    f'8
                    g'8
                }
            }
        >>

    ::

        abjad> for x in containertools.iterate_containers_forward_in_expr(staff):
        ...   x
        Staff<<2>>
        Voice{2}
        Voice{1}
        Tuplet(2/3, [e'8, f'8, g'8])

    Ignore threads.

    Return generator.
    '''

    return componenttools.iterate_components_forward_in_expr(
        expr, Container, start = start, stop = stop)
