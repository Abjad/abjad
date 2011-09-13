def get_beam_spanner_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get the only beam spanner attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> spannertools.get_beam_spanner_attached_to_component(staff[0])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> _ is beam
        True

    Return beam spanner.

    Raise missing spanner error when no beam spanner attached to `component`.

    Raise extra spanner error when more than one beam spanner attached to `component`.

    .. versionchanged:: 2.0
        renamed ``beamtools.get_beam_spanner()`` to
        ``spannertools.get_beam_spanner_attached_to_component()``.

    .. versionchanged:: 2.0
        renamed ``beamtools.get_beam_spanner_attached_to_component()`` to
        ``spannertools.get_beam_spanner_attached_to_component()``.
    '''
    from abjad.tools import spannertools

    return spannertools.get_the_only_spanner_attached_to_component(component, spannertools.BeamSpanner)
