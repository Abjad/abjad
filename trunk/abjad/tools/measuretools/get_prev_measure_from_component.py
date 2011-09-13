from abjad.tools.measuretools._get_measure_from_component import _get_measure_from_component


def get_prev_measure_from_component(component):
    '''.. versionadded:: 1.1

    Get previous measure from `component`.

    When `component` is voice, staff or other sequential context,
    and when `component` contains a measure, return last measure
    in `component`. This starts the process of backwards measure iteration. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff)
        Measure(2/8, [e'8, f'8])

    When `component` is voice, staff or other sequential context,
    and when `component` contains no measure,
    raise missing measure error.

    When `component` is a measure and there is a measure immediately
    preceeding `component`, return measure immediately preceeding component. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff[-1])
        Measure(2/8, [c'8, d'8])

    When `component` is a measure and there is no measure immediately
    preceeding `component`, return ``None``. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff[0]) is None
        True

    When `component` is a leaf and there is a measure in the parentage
    of `component`, return the measure in the parentage of `component`. ::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> measuretools.get_prev_measure_from_component(staff.leaves[0])
        Measure(2/8, [c'8, d'8])

    When `component` is a leaf and there is no measure in the parentage
    of `component`, raise missing measure error.

    .. versionchanged:: 2.0
        renamed ``iterate.measure_prev()`` to
        ``measuretools.get_prev_measure_from_component()``.
    '''

    return _get_measure_from_component(component, '_prev')
