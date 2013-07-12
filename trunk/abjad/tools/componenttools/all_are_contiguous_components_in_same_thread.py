import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_thread(
    expr, component_classes=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all contiguous components in same thread.
    Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_thread(
        ...     staff.leaves)
        True

    True when elements in `expr` are all contiguous instances 
    of `component_classes` in same thread. Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_thread(
        ...     staff.leaves, component_classes=Note)
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

    orphan_components = True
    if not first.select_parentage().is_orphan:
        orphan_components = False

    same_thread = True
    strictly_contiguous = True

    first_signature = first.select_parentage().containment_signature
    previous = first
    for current in expr[1:]:
        if not isinstance(current, component_classes):
            return False
        if not current.select_parentage().is_orphan:
            orphan_components = False
        currentrent_signature = \
            current.select_parentage().containment_signature
        if not currentrent_signature == first_signature:
            same_thread = False
        if not componenttools.is_immediate_temporal_successor_of_component(
            previous, current):
            strictly_contiguous = False
        if (not allow_orphans or 
            (allow_orphans and not orphan_components)) and \
            (not same_thread or not strictly_contiguous):
            return False
        previous = current

    return True
