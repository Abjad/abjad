def is_component_with_beam_spanner_attached(expr):
    '''.. versionadded:: 2.0

    True when `expr` is component with beam spanner attached::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = beamtools.BeamSpanner(staff.leaves)

    ::

        abjad> beamtools.is_component_with_beam_spanner_attached(staff[0])
        True

    Otherwise false::

        abjad> note = Note("c'8")

    ::

        abjad> beamtools.is_component_with_beam_spanner_attached(note)
        False

    Return boolean.

    .. versionchanged:: 2.9
        renamed ``spannertools.is_component_with_beam_spanner_attached()`` to
        ``beamtools.is_component_with_beam_spanner_attached()``.
    '''
    from abjad.tools import beamtools
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    if not isinstance(expr, componenttools.Component):
        return False

    return bool(spannertools.get_spanners_attached_to_component(expr, beamtools.BeamSpanner))
