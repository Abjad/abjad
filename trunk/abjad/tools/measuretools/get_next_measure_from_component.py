from abjad.tools.measuretools._get_measure_from_component import _get_measure_from_component


def get_next_measure_from_component(component):
    '''.. versionadded:: 1.1

    Get next measure from `component`.

    When `component` is voice, staff or other sequential context,
    and when `component` contains a measure, return first measure
    in `component`. This starts the process of forwards measure iteration. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_next_measure_from_component(staff)
        Measure(2/8, [c'8, d'8])

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise missing measure error.

    When `component` is a measure and there is a measure immediately
    following `component`, return measure immediately following component. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff[0]) is None
        True

    When `component` is a measure and there is no measure immediately
    following `component`, return ``None``. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff[-1])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff.leaves[0])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise missing measure error.

    .. versionchanged:: 2.0
        renamed ``iterate.measure_next()`` to
        ``measuretools.get_next_measure_from_component()``.
    '''

    return _get_measure_from_component(component, '_next')
