def iterate_components_forward_in_spanner(spanner, klass=None):
    '''.. versionadded:: 2.0

    .. note: Deprecated. Use `spannertools.iterate_components_in_spanner` instead.

    Yield components in `spanner` one at a time from left to right. ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> p = beamtools.BeamSpanner(t[2:])
        >>> notes = spannertools.iterate_components_forward_in_spanner(p, klass=Note)
        >>> for note in notes:
        ...   note
        Note("e'8")
        Note("f'8")

    .. versionchanged:: 2.0
        renamed ``spannertools.iterate_components_forward()`` to
        ``spannertools.iterate_components_forward_in_spanner()``.
    '''
    from abjad.tools import spannertools

    return spannertools.iterate_components_in_spanner(spanner, klass=klass)
