from abjad.tools import componenttools
from abjad.tools.skiptools.Skip import Skip


def iterate_skips_forward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate skips forward in `expr`::

        abjad> staff = Staff("<e' g' c''>8 a'8 s8 <d' f' b'>8 s2")

    ::

        abjad> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            s8
            <d' f' b'>8
            s2
        }

    ::

        abjad> for skip in skiptools.iterate_skips_forward_in_expr(staff):
        ...   skip
        Skip('s8')
        Skip('s2')

    Ignore threads.

    Return generator.
    '''

    return componenttools.iterate_components_forward_in_expr(
        expr, Skip, start = start, stop = stop)
