# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_logical_voice(
    expr, component_classes=None, allow_orphans=True):
    '''True when elements in `expr` are all contiguous components in same 
    logical voice. Otherwise false.

    ..  note:: Deprecated. Use 
        ``componenttools.all_are_logical_voice_contiguous_components()``
        instead.

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(
        ...     staff.select_leaves())
        True

    True when elements in `expr` are all contiguous instances 
    of `component_classes` in same logical voice. Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(
        ...     staff.select_leaves(), component_classes=Note)
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    return componenttools.all_are_logical_voice_contiguous_components(
        expr,
        component_classes=component_classes,
        allow_orphans=allow_orphans,
        )
