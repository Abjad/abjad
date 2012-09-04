def get_dynamic_mark_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get dynamic mark attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.DynamicMark('p')(staff[0])
        DynamicMark('p')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 \p
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.get_dynamic_mark_attached_to_component(staff[0])
        DynamicMark('p')(c'8)

    Return dynamic mark.

    Raise missing mark error when no dynamic mark attaches to `component`.

    Raise extra mark error when more than one dynamic mark attaches to `component`.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_mark_attached_to_component(component, klasses=(contexttools.DynamicMark,))
