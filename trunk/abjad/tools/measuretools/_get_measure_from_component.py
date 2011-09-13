from abjad.tools.containertools.Container import Container
from abjad.tools.measuretools.Measure import Measure
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.exceptions import MeasureContiguityError
from abjad.exceptions import MissingMeasureError
from abjad.tools.componenttools.get_proper_parentage_of_component import get_proper_parentage_of_component
from abjad.tools.componenttools.iterate_components_backward_in_expr import iterate_components_backward_in_expr
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr
from abjad.tools.measuretools._get_contemporaneous_measure import _get_contemporaneous_measure


def _get_measure_from_component(component, direction):
    '''.. versionadded:: 1.1

    When `component` is voice, staff or other sequential context,
    and when `component` contains a measure, return first measure
    in `component`.

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise :exc:`MissingMeasureError`.

    When `component` is a measure and there is a measure immediately
    following `component`, return measure immediately following component.

    When `component` is a measure and there is not measure immediately
    following `component`, raise :exc:`MeasureContiguityError`.

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`.

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise :exc:`MissingMeasureError`.
    '''

    if isinstance(component, _Leaf):
        for parent in get_proper_parentage_of_component(component):
            if isinstance(parent, Measure):
                return parent
        raise MissingMeasureError
    elif isinstance(component, Measure):
        if direction == '_next':
            return component._navigator._next_namesake
        elif direction == '_prev':
            return component._navigator._prev_namesake
        else:
            raise ValueError('direction must be _next or _prev.')
    elif isinstance(component, Container):
        return _get_contemporaneous_measure(component, direction)
    elif isinstance(component, (list, tuple)):
        if direction == '_next':
            measure_generator = iterate_components_forward_in_expr(component, Measure)
        elif direction == '_prev':
            measure_generator = iterate_components_backward_in_expr(component, Measure)
        else:
            raise ValueError('direction must be _next or _prev.')
        try:
            measure = measure_generator.next()
            return measure
        except StopIteration:
            raise MissingMeasureError
    else:
        raise TypeError('"%s" is unknown Abjad component.' % component)
