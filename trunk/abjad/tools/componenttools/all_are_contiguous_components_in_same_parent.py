import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_parent(expr, classes=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all contiguous components in same parent.
    Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_parent(staff.leaves)
        True

    True when elements in `expr` are all contiguous `classes` in same parent.
    Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_parent(staff.leaves, classes=Note)
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    if not isinstance(expr, (list, tuple, types.GeneratorType, selectiontools.Selection)):
        return False

    if classes is None:
        classes = componenttools.Component

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, classes):
        return False

    first_parent = first._parent
    if first_parent is None:
        if allow_orphans:
            orphan_components = True
        else:
            return False

    same_parent = True
    strictly_contiguous = True

    prev = first
    for cur in expr[1:]:
        if not isinstance(cur, classes):
            return False
        if not cur.parentage.is_orphan:
            orphan_components = False
        if not cur._parent is first_parent:
            same_parent = False
        if not componenttools.is_immediate_temporal_successor_of_component(prev, cur):
            strictly_contiguous = False
        if (not allow_orphans or (allow_orphans and not orphan_components)) and \
            (not same_parent or not strictly_contiguous):
            return False
        prev = cur

    return True
