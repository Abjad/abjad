from abjad.tools.componenttools.iterate_namesakes_backward_from_component import iterate_namesakes_backward_from_component
from abjad.tools.componenttools.iterate_namesakes_forward_from_component import iterate_namesakes_forward_from_component


def get_nth_namesake_from_component(component, n):
    '''.. versionadded:: 2.0

    For positive `n`, return namesake to the right of `component`::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> componenttools.get_nth_namesake_from_component(t[1], 1)
        Note("e'8")

    For negative `n`, return namesake to the left of `component`::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> componenttools.get_nth_namesake_from_component(t[1], -1)
        Note("c'8")

    Return `component` when `n` is zero::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> componenttools.get_nth_namesake_from_component(t[1], 0)
        Note("d'8")

    Return component or none.
    '''

    if 0 <= n:
        for i, namesake in enumerate(iterate_namesakes_forward_from_component(component)):
            if i == n:
                return namesake
    else:
        n = abs(n)
        for i, namesake in enumerate(iterate_namesakes_backward_from_component(component)):
            if i == n:
                return namesake

    raise IndexError('only %s namesakes from %s, not %s.' % (i, component, n))
