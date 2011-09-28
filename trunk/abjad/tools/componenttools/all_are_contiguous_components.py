from abjad.tools.componenttools._Component import _Component
from abjad.tools.componenttools.is_orphan_component import is_orphan_component
import types


def all_are_contiguous_components(expr, klasses=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all contiguous components. Otherwise false::

        abjad> staff = Staff("c'8 d'8 e'8")
        abjad> componenttools.all_are_contiguous_components(staff.leaves)
        True

    True when elements in `expr` are all contiguous `klasses`. Otherwise false::

        abjad> staff = Staff("c'8 d'8 e'8")
        abjad> componenttools.all_are_contiguous_components(staff.leaves, klasses = Note)
        True

    Return boolean.
    '''

    if not isinstance(expr, (list, tuple, types.GeneratorType)):
        #raise TypeError('Must be list of Abjad components.')
        return False

    if klasses is None:
        klasses = _Component

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, klasses):
        return False

    orphan_components = True
    if not is_orphan_component(first):
        orphan_components = False

    strictly_contiguous = True

    prev = first
    for cur in expr[1:]:
        if not isinstance(cur, klasses):
            return False
        if not is_orphan_component(cur):
            orphan_components = False
        if not prev._navigator._is_immediate_temporal_successor_of(cur):
            strictly_contiguous = False
        if (not allow_orphans or (allow_orphans and not orphan_components)) and \
            not strictly_contiguous:
            return False
        prev = cur

    return True
