from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import leaftools


def get_previous_measure_from_component(component):
    '''.. versionadded:: 1.1

    Get previous measure from `component`.

    When `component` is voice, staff or other sequential context,
    and when `component` contains a measure, return last measure
    in `component`. This starts the process of backwards measure iteration. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff)
        Measure(2/8, [e'8, f'8])

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise missing measure error.

    When `component` is a measure and there is a measure immediately
    preceeding `component`, return measure immediately preceeding component. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff[-1])
        Measure(2/8, [c'8, d'8])

    When `component` is a measure and there is no measure immediately
    preceeding `component`, return ``None``. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff[0]) is None
        True

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff.leaves[0])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise missing measure error.

    .. versionchanged:: 2.0
        renamed ``iterate.measure_prev()`` to
        ``measuretools.get_previous_measure_from_component()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import measuretools

    if isinstance(component, leaftools.Leaf):
        for parent in componenttools.get_proper_parentage_of_component(component):
            if isinstance(parent, measuretools.Measure):
                return parent
        raise MissingMeasureError
    elif isinstance(component, measuretools.Measure):
        return componenttools.get_nth_namesake_from_component(component, -1)
    elif isinstance(component, containertools.Container):
        return measuretools.get_measure_that_stops_with_container(component)
    elif isinstance(component, (list, tuple)):
        measure_generator = iterationtools.iterate_measures_in_expr(component, reverse=True)
        try:
            measure = measure_generator.next()
            return measure
        except StopIteration:
            raise MissingMeasureError
    else:
        raise TypeError('"%s" is unknown Abjad component.' % component)
