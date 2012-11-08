from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import leaftools


def get_next_measure_from_component(component):
    '''.. versionadded:: 1.1

    Get next measure from `component`.

    When `component` is a voice, staff or other sequential context,
    and when `component` contains a measure, return first measure
    in `component`. This starts the process of forwards measure iteration. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_next_measure_from_component(staff)
        Measure(2/8, [c'8, d'8])

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise missing measure error.

    When `component` is a measure and there is a measure immediately
    following `component`, return measure immediately following component. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff[0]) is None
        True

    When `component` is a measure and there is no measure immediately
    following `component`, return ``None``. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff[-1])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`. ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> measuretools.get_previous_measure_from_component(staff.leaves[0])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise missing measure error.

    .. versionchanged:: 2.0
        renamed ``iterate.measure_next()`` to
        ``measuretools.get_next_measure_from_component()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import iterationtools
    from abjad.tools import measuretools

    if isinstance(component, leaftools.Leaf):
        for parent in componenttools.get_proper_parentage_of_component(component):
            if isinstance(parent, measuretools.Measure):
                return parent
        raise MissingMeasureError
    elif isinstance(component, measuretools.Measure):
        return componenttools.get_nth_namesake_from_component(component, 1)
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
        raise TypeError('"%s" is unknown Abjad component.' % component)
