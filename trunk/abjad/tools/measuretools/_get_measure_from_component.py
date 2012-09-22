from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import leaftools


# TODO: make public
# TODO: replace string-value 'direction' variable with Left or Right constants
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
    from abjad.tools import iterationtools
    from abjad.tools import measuretools
    from abjad.tools.measuretools._get_contemporaneous_measure import _get_contemporaneous_measure

    if isinstance(component, leaftools.Leaf):
        for parent in componenttools.get_proper_parentage_of_component(component):
            if isinstance(parent, measuretools.Measure):
                return parent
        raise MissingMeasureError
    elif isinstance(component, measuretools.Measure):
        if direction == '_next':
            return componenttools.get_nth_namesake_from_component(component, 1)
        elif direction == '_prev':
            return componenttools.get_nth_namesake_from_component(component, -1)
        else:
            raise ValueError('direction must be _next or _prev.')
    elif isinstance(component, containertools.Container):
        return _get_contemporaneous_measure(component, direction)
    elif isinstance(component, (list, tuple)):
        if direction == '_next':
            #measure_generator = iterate_components_in_expr(component, measuretools.Measure)
            measure_generator = iterationtools.iterate_measures_in_expr(component)
        elif direction == '_prev':
            #measure_generator = iterate_components_backward_in_expr(component, measuretools.Measure)
            measure_generator = iterationtools.iterate_measures_in_expr(component, reverse=True)
        else:
            raise ValueError('direction must be _next or _prev.')
        try:
            measure = measure_generator.next()
            return measure
        except StopIteration:
            raise MissingMeasureError
    else:
        raise TypeError('"%s" is unknown Abjad component.' % component)
