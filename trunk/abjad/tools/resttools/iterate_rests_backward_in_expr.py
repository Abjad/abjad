from abjad.tools.resttools.Rest import Rest
from abjad.tools import componenttools


def iterate_rests_backward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate rests backward in `expr`::

        abjad> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    ::

        abjad> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            r8
            <d' f' b'>8
            r2
        }

    ::

        abjad> for rest in resttools.iterate_rests_backward_in_expr(staff):
        ...   rest
        Rest('r2')
        Rest('r8')

    Ignore threads.

    Return generator.
    '''

    return componenttools.iterate_components_backward_in_expr(
        expr, Rest, start = start, stop = stop)
