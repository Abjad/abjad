def destroy_spanners_attached_to_components_in_expr(expr, klass=None):
    r'''.. versionadded:: 2.9

    Destroy spanners of `klass` attached to components in `expr`::

        >>> staff = Staff("c'4 [ ( d' e' f' ) ]")

    ::

        >>> f(staff)
        \new Staff {
            c'4 [ (
            d'4
            e'4
            f'4 ] )
        }

    ::

        >>> spanners = spannertools.destroy_spanners_attached_to_components_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more empty spanners.

    Order of spanners in return value can not be predicted.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    result = []
    for component in iterationtools.iterate_components_in_expr(expr):
        result.extend(spannertools.destroy_spanners_attached_to_component(component, klass=klass))

    return tuple(result)
