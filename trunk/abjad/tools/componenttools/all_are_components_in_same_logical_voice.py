# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_components_in_same_logical_voice(expr, classes=None, allow_orphans=True):
    '''True when elements in `expr` are all components in same logical voice. 
    Otherwise false:

    ::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> componenttools.all_are_components_in_same_logical_voice(voice.select_leaves())
        True

    True when elements in `expr` are all `classes` in same logical voice. 
    Otherwise false:

    ::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> componenttools.all_are_components_in_same_logical_voice(
        ...     voice.select_leaves(), classes=Note)
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

    if classes is None:
        classes = componenttools.Component

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, classes):
        return False

    orphan_components = True
    if not first._select_parentage().is_orphan:
        orphan_components = False

    same_logical_voice = True

    first_signature = first._select_parentage().logical_voice_indicator
    for component in expr[1:]:
        parentage = component._select_parentage()
        if not parentage.is_orphan:
            orphan_components = False
        if not allow_orphans and orphan_components:
            return False
        if parentage.logical_voice_indicator != first_signature:
            same_logical_voice = False
        if not allow_orphans and not same_logical_voice:
            return False
        if allow_orphans and not orphan_components and not same_logical_voice:
            return False

    return True
