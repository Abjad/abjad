# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_parent(
    expr, component_classes=None, allow_orphans=True):
    '''True when elements in `expr` are all contiguous components in same parent.
    Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_parent(
        ...     staff.select_leaves())
        True

    True when elements in `expr` are all contiguous instances
    of `component_classes` in same parent. Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_parent(
        ...     staff.select_leaves(), component_classes=(Note,))
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    allowable_types = (
        list,
        tuple,
        types.GeneratorType,
        selectiontools.Selection,
        )

    if not isinstance(expr, allowable_types):
        return False

    component_classes = component_classes or (componenttools.Component, )
    if not isinstance(component_classes, tuple):
        component_classes = (component_classes, )
    assert isinstance(component_classes, tuple)

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, component_classes):
        return False

    first_parent = first._parent
    if first_parent is None:
        if allow_orphans:
            orphan_components = True
        else:
            return False

    same_parent = True
    strictly_contiguous = True

    previous = first
    for current in expr[1:]:
        if not isinstance(current, component_classes):
            return False
        if not current.select_parentage().is_orphan:
            orphan_components = False
        if not current._parent is first_parent:
            same_parent = False
        if not previous._is_immediate_temporal_successor_of(current):
            strictly_contiguous = False
        if (not allow_orphans or 
            (allow_orphans and not orphan_components)) and \
            (not same_parent or not strictly_contiguous):
            return False
        previous = current

    return True
