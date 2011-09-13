def is_component_with_spanner_attached(expr, klass = None):
    r'''.. versionadded:: 2.0

    True when `expr` is a component with spanner attached::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> spannertools.is_component_with_spanner_attached(staff[0])
        True

    Otherwise false::

        abjad> spannertools.is_component_with_spanner_attached(staff)
        False

    When `klass` is not none then true when `expr` is a component
    with a spanner of `klass` attached.

    Return true or false.
    '''
    from abjad.tools.componenttools._Component import _Component

    if isinstance(expr, _Component):
        if klass is None:
            #return 0 < len(expr.spanners.attached)
            #return 0 < len(expr.spanners._spanners)
            return 0 < len(expr.spanners)
        else:
            #for spanner in expr.spanners.attached:
            #for spanner in expr.spanners._spanners:
            for spanner in expr.spanners:
                if isinstance(spanner, klass):
                    return True
    return False
