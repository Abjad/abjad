from abjad.tools.spannertools.destroy_spanners_attached_to_component import destroy_spanners_attached_to_component


def destroy_spanners_attached_to_components_in_expr(expr, klass=None):
    r'''.. versionadded:: 2.9

    Destroy spanners of `klass` attached to components in `expr`::

        abjad> staff = Staff("c'4 [ ( d' e' f' ) ]")

    ::

        abjad> f(staff)
        \new Staff {
            c'4 [ (
            d'4
            e'4
            f'4 ] )
        }

    ::

        abjad> spanners = spannertools.destroy_spanners_attached_to_components_in_expr(staff)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more empty spanners.

    Order of spanners in return value can not be predicted.
    '''
    from abjad.tools import componenttools

    result = []
    for component in componenttools.iterate_components_forward_in_expr(expr):
        result.extend(destroy_spanners_attached_to_component(component, klass=klass))

    return tuple(result)
