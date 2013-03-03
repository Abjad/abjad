def iterate_components_and_grace_containers_in_expr(expr, klass):
    r'''Iterate components of `klass` forward in `expr`::

        >>> voice = Voice("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(voice[:])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> grace_notes = [Note("c'16"), Note("d'16")]
        >>> gracetools.GraceContainer(grace_notes, kind='grace')(voice[1])
        Note("d'8")

    ::

        >>> after_grace_notes = [Note("e'16"), Note("f'16")]
        >>> gracetools.GraceContainer(after_grace_notes, kind='after')(voice[1])
        Note("d'8")

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            \grace {
                c'16
                d'16
            }
            \afterGrace
            d'8
            {
                e'16
                f'16
            }
            e'8
            f'8 ]
        }

    ::

        >>> x = iterationtools.iterate_components_and_grace_containers_in_expr(voice, Note)
        >>> for note in x:
        ...     note
        ...
        Note("c'8")
        Note("c'16")
        Note("d'16")
        Note("d'8")
        Note("e'16")
        Note("f'16")
        Note("e'8")
        Note("f'8")

    Include grace leaves before main leaves.

    Include grace leaves after main leaves.
    '''
    if hasattr(expr, '_grace'):
        for m in expr.grace:
            for x in iterate_components_and_grace_containers_in_expr(m, klass):
                yield x
        if isinstance(expr, klass):
            yield expr
    if hasattr(expr, '_after_grace'):
        for m in expr.after_grace:
            for x in iterate_components_and_grace_containers_in_expr(m, klass):
                yield x
    elif isinstance(expr, klass):
        yield expr
    if isinstance(expr, (list, tuple)):
        for m in expr:
            for x in iterate_components_and_grace_containers_in_expr(m, klass):
                yield x
    if hasattr(expr, '_music'):
        for m in expr._music:
            for x in iterate_components_and_grace_containers_in_expr(m, klass):
                yield x
