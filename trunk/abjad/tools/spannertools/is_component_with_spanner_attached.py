from abjad.tools import componenttools


def is_component_with_spanner_attached(expr, klass=None):
    r'''.. versionadded:: 2.0

    True when `expr` is a component with spanner attached::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)
        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> spannertools.is_component_with_spanner_attached(staff[0])
        True

    Otherwise false::

        >>> spannertools.is_component_with_spanner_attached(staff)
        False

    When `klass` is not none then true when `expr` is a component
    with a spanner of `klass` attached.

    Return true or false.
    '''
    if isinstance(expr, componenttools.Component):
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
