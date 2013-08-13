# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_contiguous_components_in_same_logical_voice(
    expr, component_classes=None, allow_orphans=True):
    r'''True when elements in `expr` are all logical-voice-contiguous components:

    ::

        >>> container_1 = Container("c'8 d'8")
        >>> inner_voice = Voice("e'8 f'8")
        >>> container_2 = Container("g'8 a'8")
        >>> outer_voice = Voice([container_1, inner_voice, container_2])
        >>> show(outer_voice) # doctest: +SKIP

    ..  doctest::

        >>> f(outer_voice)
        \new Voice {
            {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }

    ::

        >>> show(outer_voice) # doctest: +SKIP

    The first two notes belong to the same logical voice 
    and are time-contiguous:

        >>> components = container_1.select_leaves()
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(components)
        True

    The middle two notes belong to the same logical voice 
    and are time-contiguous:

        >>> components = inner_voice.select_leaves()
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(components)
        True

    The middle two notes belong to the same logical voice 
    and are time-contiguous:

        >>> components = container_1.select_leaves()
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(components)
        True

    But the six leaves taken together belong to different logical voices:

        >>> components = outer_voice.select_leaves(
        ...     allow_discontiguous_leaves=True)
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(components)
        False

    The first two leaves and the last two leaves belong to the same logical
    voice. But the first two leaves and the last two leaves are not
    time-contiguous:

        >>> container_1_leaves = container_1.select_leaves()
        >>> container_2_leaves = container_2.select_leaves()
        >>> leaves = container_1_leaves + container_2_leaves
        >>> componenttools.all_are_contiguous_components_in_same_logical_voice(
        ...     components)
        False

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

    first_parentage = first._select_parentage()
    first_containment_signature = first_parentage.containment_signature
    first_root = first_containment_signature._root
    total_orphan_components = 0
    if first._select_parentage().is_orphan:
        total_orphan_components += 1
    previous = first
    for current in expr[1:]:
        current_parentage = current._select_parentage()
        current_containment_signature = current_parentage.containment_signature
        current_root = current_containment_signature._root
        if current_parentage.is_orphan:
            total_orphan_components += 1
        # false if wrong type of component found
        if not isinstance(current, component_classes):
            return False
        # false if multiple orphan components appear in input
        if not allow_orphans and 1 < total_orphan_components:
            return False
        # false if nonorphan components in different logical voices
        if current_containment_signature != first_containment_signature:
            return False
        # false if components in same logical voice are discontiguous
        if current_containment_signature._root == first_root:
            if not previous._is_immediate_temporal_successor_of(current):
                return False
        previous = current

    return True
