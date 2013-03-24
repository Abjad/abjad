def find_index_of_spanner_component_at_score_offset(spanner, score_offset):
    r'''Return index of component in 'spanner' that begins at exactly 'score_offset'::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> spannertools.find_index_of_spanner_component_at_score_offset(beam, Duration(3, 8))
        3

    Raise spanner population error when no component in `spanner` begins at exactly `score_offset`.
    '''

    for component in spanner:
        if component.timespan.start_offset == score_offset:
            return spanner.index(component)

    raise SpannerPopulationError('no component in spanner at this score offset.')
