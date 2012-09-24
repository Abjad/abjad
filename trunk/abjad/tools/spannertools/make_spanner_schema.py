def make_spanner_schema(components):
    r'''.. versionadded:: 2.0

    Make schema of spanners contained by `components`::

        >>> voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
        >>> beam = beamtools.BeamSpanner(voice.leaves[:4])
        >>> slur = spannertools.SlurSpanner(voice[-2:])

    ::

        >>> f(voice)
        \new Voice {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
            {
                g'8 (
                a'8
            }
            {
                b'8
                c''8 )
            }
        }

    ::

        >>> spannertools.make_spanner_schema(voice.leaves[2:4])
        {BeamSpanner(c'8, d'8, e'8, f'8): [0, 1]}

    Return dictionary.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    schema = {}
    spanners_contained_by_components = spannertools.get_spanners_contained_by_components(components)
    for spanner in spanners_contained_by_components:
        schema[spanner] = []

    for i, component in enumerate(iterationtools.iterate_components_in_expr(components)):
        attached_spanners = spannertools.get_spanners_attached_to_component(component)
        for attached_spanner in attached_spanners:
            try:
                schema[attached_spanner].append(i)
            except KeyError:
                pass

    return schema
