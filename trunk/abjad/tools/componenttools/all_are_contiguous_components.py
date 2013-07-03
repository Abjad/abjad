import types
from abjad.tools import selectiontools


def all_are_contiguous_components(expr, classes=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all contiguous components. Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components(staff.leaves)
        True

    True when elements in `expr` are all contiguous `classes`. Otherwise false:

    ::

        >>> staff = Staff("c'8 d'8 e'8")
        >>> componenttools.all_are_contiguous_components(staff.leaves, classes=Note)
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    if not isinstance(expr, (list, tuple, types.GeneratorType, selectiontools.Selection)):
        #raise TypeError('Must be list of Abjad components.')
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

    strictly_contiguous = True

    prev = first
    for cur in expr[1:]:
        if not isinstance(cur, classes):
            return False
        if not cur.parentage.is_orphan:
            orphan_components = False
        if not componenttools.is_immediate_temporal_successor_of_component(prev, cur):
            strictly_contiguous = False
        if (not allow_orphans or (allow_orphans and not orphan_components)) and \
            not strictly_contiguous:
            return False
        prev = cur

    return True
