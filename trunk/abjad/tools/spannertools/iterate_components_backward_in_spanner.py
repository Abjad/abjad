from abjad.tools import componenttools


def iterate_components_backward_in_spanner(spanner, klass=None):
    '''.. versionadded:: 2.0

    Yield components in `spanner` one at a time from left to right. ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> p = beamtools.BeamSpanner(t[2:])

    ::

        >>> notes = spannertools.iterate_components_backward_in_spanner(p, klass=Note)

    ::

        >>> for note in notes:
        ...   note
        Note("f'8")
        Note("e'8")

    .. versionchanged:: 2.0
        renamed ``spannertools.iterate_components_backward()`` to
        ``spannertools.iterate_components_backward_in_spanner()``.
    '''
    from abjad.tools import spannertools

    if not isinstance(spanner, spannertools.Spanner):
        raise TypeError

    klass = klass or componenttools.Component

    for component in reversed(spanner._components):
        dfs = componenttools.iterate_components_depth_first(component, direction=Right)
        for node in dfs:
            if isinstance(node, klass):
                yield node
