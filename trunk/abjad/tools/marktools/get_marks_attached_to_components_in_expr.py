from abjad.tools.marktools.get_marks_attached_to_component import get_marks_attached_to_component


def get_marks_attached_to_components_in_expr(expr):
    r'''.. versionadded:: 2.9

    Get marks attached to components in `expr`::

        >>> staff = Staff(r"c'4 \pp d' \staccato e' \ff f' \staccato")

    ::

        \new Staff {
            c'4 \pp
            d'4 -\staccato
            e'4 \ff
            f'4 -\staccato
        }

    ::

        >>> marktools.get_marks_attached_to_components_in_expr(staff)
        (DynamicMark('pp')(c'4), Articulation('staccato')(d'4), DynamicMark('ff')(e'4), Articulation('staccato')(f'4))

    Return tuple of zero or more marks.
    '''
    from abjad.tools import componenttools

    result = []
    for component in componenttools.iterate_components_forward_in_expr(expr):
        result.extend(get_marks_attached_to_component(component))

    return tuple(result)
