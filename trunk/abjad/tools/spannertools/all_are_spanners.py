def all_are_spanners(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad spanners::

        >>> voice = Voice("c'8 d'8 e'8 f'8")
        >>> spanner = beamtools.BeamSpanner(voice[:2])

    ::

        >>> spannertools.all_are_spanners([spanner])
        True

    True when `expr` is an empty sequence::

        >>> spannertools.all_are_spanners([])
        True

    Otherwise false::

        >>> spannertools.all_are_spanners('foo')
        False

    Return boolean.
    '''
    from abjad.tools import spannertools

    return all([isinstance(x, spannertools.Spanner) for x in expr])
