def find_spanner_component_starting_at_exactly_score_offset(spanner, score_offset):
    r'''Find `spanner` component starting at exactly `score_offset`::

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

        abjad> spannertools.find_spanner_component_starting_at_exactly_score_offset(beam, Duration(3, 8))
        Note("f'8")

    When no `spanner` component starts at exactly `score_offset` return none.

    Return `spanner` component or none.

    .. versionchanged:: 2.0
        renamed ``spannertools.find_component_at_score_offset()`` to
        ``spannertools.find_spanner_component_starting_at_exactly_score_offset()``.
    '''

    for component in spanner:
        if component._offset.start == score_offset:
            return component
