# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def get_next_measure_from_component(component):
    '''Get next measure from `component`.

    When `component` is a voice, staff or other sequential context,
    and when `component` contains a measure, return first measure
    in `component`. This starts the process of forwards measure iteration.

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> scoretools.get_next_measure_from_component(staff)
        Measure((2, 8), "c'8 d'8")

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise missing measure error.

    When `component` is a measure and there is a measure immediately
    following `component`, return measure immediately following component.

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> scoretools.get_previous_measure_from_component(staff[0]) is None
        True

    When `component` is a measure and there is no measure immediately
    following `component`, return ``None``.

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> scoretools.get_previous_measure_from_component(staff[-1])
        Measure((2, 8), "c'8 d'8")

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`.

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> selector = select().by_leaf(flatten=True)
        >>> leaves = selector(staff)
        >>> scoretools.get_previous_measure_from_component(leaves[0])
        Measure((2, 8), "c'8 d'8")

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise missing measure error.
    '''
    from abjad.tools import scoretools

    if isinstance(component, scoretools.Leaf):
        for parent in component._get_parentage(include_self=False):
            if isinstance(parent, scoretools.Measure):
                return parent
        raise MissingMeasureError
    elif isinstance(component, scoretools.Measure):
        return component._get_in_my_logical_voice(
            1, prototype=scoretools.Measure)
    elif isinstance(component, scoretools.Container):
        return scoretools.get_measure_that_starts_with_container(component)
    elif isinstance(component, (list, tuple)):
        measure_generator = iterate(component).by_class(scoretools.Measure)
        try:
            measure = next(measure_generator)
            return measure
        except StopIteration:
            raise MissingMeasureError
    else:
        message = 'unknown component: {!r}.'
        raise TypeError(message.format(component))