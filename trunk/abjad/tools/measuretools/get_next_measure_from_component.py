# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import leaftools


def get_next_measure_from_component(component):
    '''Get next measure from `component`.

    When `component` is a voice, staff or other sequential context,
    and when `component` contains a measure, return first measure
    in `component`. This starts the process of forwards measure iteration.
    
    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> measuretools.get_next_measure_from_component(staff)
        Measure(2/8, [c'8, d'8])

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise missing measure error.

    When `component` is a measure and there is a measure immediately
    following `component`, return measure immediately following component.
    
    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> measuretools.get_previous_measure_from_component(staff[0]) is None
        True

    When `component` is a measure and there is no measure immediately
    following `component`, return ``None``.
    
    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> measuretools.get_previous_measure_from_component(staff[-1])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`.
    
    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> measuretools.get_previous_measure_from_component(staff.select_leaves()[0])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise missing measure error.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import iterationtools
    from abjad.tools import measuretools

    if isinstance(component, leaftools.Leaf):
        for parent in component._get_parentage(include_self=False):
            if isinstance(parent, measuretools.Measure):
                return parent
        raise MissingMeasureError
    elif isinstance(component, measuretools.Measure):
        return component._get_in_my_logical_voice(
            1, component_class=measuretools.Measure)
    elif isinstance(component, containertools.Container):
        return measuretools.get_measure_that_starts_with_container(component)
    elif isinstance(component, (list, tuple)):
        measure_generator = iterationtools.iterate_measures_in_expr(component)
        try:
            measure = measure_generator.next()
            return measure
        except StopIteration:
            raise MissingMeasureError
    else:
        message = 'unknown component: {!r}.'
        raise TypeError(message.format(component))
