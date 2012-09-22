def get_nth_namesake_from_component(component, n):
    '''.. versionadded:: 2.0

    For positive `n`, return namesake to the right of `component`::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> componenttools.get_nth_namesake_from_component(t[1], 1)
        Note("e'8")

    For negative `n`, return namesake to the left of `component`::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> componenttools.get_nth_namesake_from_component(t[1], -1)
        Note("c'8")

    Return `component` when `n` is zero::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> componenttools.get_nth_namesake_from_component(t[1], 0)
        Note("d'8")

    Return component or none.
    '''
    from abjad.tools import iterationtools

    if 0 <= n:
        for i, namesake in enumerate(iterationtools.iterate_namesakes_from_component(component)):
            if i == n:
                return namesake
    else:
        n = abs(n)
        for i, namesake in enumerate(iterationtools.iterate_namesakes_from_component(component, reverse=True)):
            if i == n:
                return namesake
