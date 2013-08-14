# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_logical_voice(
    expr, component_classes=None, allow_orphans=True):
    r'''True when all elements in `expr` are contiguous components
    in the same logical voice. Otherwise false.

    .. note:: Deprecated.

    Returns boolean.
    '''
    from abjad.tools import componenttools

    raise Exception

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

    all_are_orphans_of_correct_type = True
    if allow_orphans:
        for component in expr:
            if not isinstance(component, component_classes):
                all_are_orphans_of_correct_type = False
                break
            if not component._select_parentage().is_orphan:
                all_are_orphans_of_correct_type = False
                break
        if all_are_orphans_of_correct_type:
            return True

    if not allow_orphans:
        if any(x._select_parentage().is_orphan for x in expr):
            return False

    first = expr[0]
    if not isinstance(first, component_classes):
        return False

    first_parentage = first._select_parentage()
    first_logical_voice_indicator = first_parentage.logical_voice_indicator
    first_root = first_parentage.root
    previous = first
    for current in expr[1:]:
        current_parentage = current._select_parentage()
        current_logical_voice_indicator = \
            current_parentage.logical_voice_indicator
        # false if wrong type of component found
        if not isinstance(current, component_classes):
            return False
        # false if in different logical voices
        if current_logical_voice_indicator != first_logical_voice_indicator:
            return False
        # false if components are in same score and are discontiguous
        if current_parentage.root == first_root:
            if not previous._is_immediate_temporal_successor_of(current):
                return False
        previous = current

    return True
