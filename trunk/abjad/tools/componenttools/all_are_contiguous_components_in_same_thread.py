import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_thread(expr, classes=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all contiguous components in same thread.
    Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_thread(staff.leaves)
        True

    True when elements in `expr` are all contiguous `classes` in same thread.
    Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components_in_same_thread(staff.leaves, classes=Note)
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

    orphan_components = True
    if not first.parentage.is_orphan:
        orphan_components = False

    same_thread = True
    strictly_contiguous = True

    first_signature = first.parentage.containment_signature
    prev = first
    for cur in expr[1:]:
        if not isinstance(cur, classes):
            return False
        if not cur.parentage.is_orphan:
            orphan_components = False
        current_signature = cur.parentage.containment_signature
        if not current_signature == first_signature:
            same_thread = False
        if not componenttools.is_immediate_temporal_successor_of_component(prev, cur):
            strictly_contiguous = False
        if (not allow_orphans or (allow_orphans and not orphan_components)) and \
            (not same_thread or not strictly_contiguous):
            return False
        prev = cur

    return True
