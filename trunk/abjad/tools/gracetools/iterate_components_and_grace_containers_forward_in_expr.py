def iterate_components_and_grace_containers_forward_in_expr(expr, klass):
    r'''Iterate components of `klass` forward in `expr`::

        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(voice[:])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> grace_notes = [Note("c'16"), Note("d'16")]
        abjad> gracetools.Grace(grace_notes, kind = 'grace')(voice[1])
        Note("d'8")

    ::

        abjad> after_grace_notes = [Note("e'16"), Note("f'16")]
        abjad> gracetools.Grace(after_grace_notes, kind = 'after')(voice[1])
        Note("d'8")

    ::

        abjad> f(voice)
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

        abjad> for note in gracetools.iterate_components_and_grace_containers_forward_in_expr(voice, Note):
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

    .. versionchanged:: 2.0
        renamed ``iterate.grace()`` to
        ``componenttools.iterate_components_and_grace_containers_forward_in_expr()``.
    '''

#   if hasattr(expr, 'grace'):
#      for m in expr.grace.before:
#         for x in iterate_components_and_grace_containers_forward_in_expr(m, klass):
#            yield x
#      if isinstance(expr, klass):
#         yield expr
#      for m in expr.grace.after:
#         for x in iterate_components_and_grace_containers_forward_in_expr(m, klass):
#            yield x

    if hasattr(expr, '_grace'):
        for m in expr.grace:
            for x in iterate_components_and_grace_containers_forward_in_expr(m, klass):
                yield x
        if isinstance(expr, klass):
            yield expr
    if hasattr(expr, '_after_grace'):
        for m in expr.after_grace:
            for x in iterate_components_and_grace_containers_forward_in_expr(m, klass):
                yield x
    elif isinstance(expr, klass):
        yield expr
    if isinstance(expr, (list, tuple)):
        for m in expr:
            for x in iterate_components_and_grace_containers_forward_in_expr(m, klass):
                yield x
    if hasattr(expr, '_music'):
        for m in expr._music:
            for x in iterate_components_and_grace_containers_forward_in_expr(m, klass):
                yield x
