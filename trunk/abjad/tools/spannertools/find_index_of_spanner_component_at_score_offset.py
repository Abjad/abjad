from abjad.exceptions import SpannerPopulationError


def find_index_of_spanner_component_at_score_offset(spanner, score_offset):
    r'''Return index of component in 'spanner' that begins at exactly 'score_offset'::

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

        abjad> spannertools.find_index_of_spanner_component_at_score_offset(beam, Duration(3, 8))
        3

    Raise spanner population error when no component in `spanner` begins at exactly `score_offset`.

    .. versionchanged:: 2.0
        renamed ``spannertools.find_index_at_score_offset()`` to
        ``spannertools.find_index_of_spanner_component_at_score_offset()``.
    '''

    for component in spanner:
        if component._offset.start == score_offset:
            return spanner.index(component)

    raise SpannerPopulationError('no component in spanner at this score offset.')
