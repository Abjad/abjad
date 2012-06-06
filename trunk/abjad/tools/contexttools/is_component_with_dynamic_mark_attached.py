from abjad.tools.contexttools.DynamicMark import DynamicMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_dynamic_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component and has a dynamic mark attached::

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

        >>> contexttools.is_component_with_dynamic_mark_attached(staff[0])
        True

    Otherwise false::

        >>> contexttools.is_component_with_dynamic_mark_attached(staff)
        False

    Return boolean.
    '''

    return is_component_with_context_mark_attached(expr, (DynamicMark,))
