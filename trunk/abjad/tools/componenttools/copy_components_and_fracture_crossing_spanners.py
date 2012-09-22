import copy


def copy_components_and_fracture_crossing_spanners(components, n=1):
    r'''.. versionadded:: 1.1

    Copy `components` and fracture crossing spanners.

    The `components` must be thread-contiguous.

    The steps this function takes are as follows.
    Deep copy `components`.
    Deep copy spanners that attach to any component in `components`.
    Fracture spanners that attach to components not in `components`.
    Return Python list of copied components. ::

        >>> voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
        >>> beam = beamtools.BeamSpanner(voice.leaves[:4])
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
                g'8
                a'8
            }
        }

    ::

        >>> result = componenttools.copy_components_and_fracture_crossing_spanners(
        ...     voice.leaves[2:4])
        >>> result
        (Note("e'8"), Note("f'8"))

    ::

        >>> new_voice = Voice(result)
        >>> f(new_voice)
        \new Voice {
            e'8 [
            f'8 ]
        }

    ::

        >>> voice.leaves[2] is new_voice.leaves[0]
        False

    Copy `components` a total of `n` times. ::

        >>> result = componenttools.copy_components_and_fracture_crossing_spanners(
        ...     voice.leaves[2:4], n=3)
        >>> result
        (Note("e'8"), Note("f'8"), Note("e'8"), Note("f'8"), Note("e'8"), Note("f'8"))

    ::

        >>> new_voice = Voice(result)
        >>> f(new_voice)
        \new Voice {
            e'8 [
            f'8 ]
            e'8 [
            f'8 ]
            e'8 [
            f'8 ]
        }

    .. versionchanged:: 2.0
        renamed ``clone.fracture()`` to
        ``componenttools.copy_components_and_fracture_crossing_spanners()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_components_and_fracture_crossing_spanners()`` to
        ``componenttools.copy_components_and_fracture_crossing_spanners()``.
    '''
    from abjad.tools import spannertools
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools.componenttools._ignore_parentage_of_components import \
        _ignore_parentage_of_components
    from abjad.tools.componenttools._restore_parentage_to_components_by_receipt import \
        _restore_parentage_to_components_by_receipt
    from abjad.tools.marktools._reattach_blinded_marks_to_components_in_expr import \
        _reattach_blinded_marks_to_components_in_expr

    if n < 1:
        return []

    assert componenttools.all_are_thread_contiguous_components(components)

    new_components = copy.deepcopy(components)

    # make schema of spanners contained by components
    schema = spannertools.make_spanner_schema(components)

    # copy spanners covered by components
    for covered_spanner, component_indices in schema.items():
        new_covered_spanner = copy.copy(covered_spanner)
        del(schema[covered_spanner])
        schema[new_covered_spanner] = component_indices

    # reverse schema
    reversed_schema = {}
    for new_covered_spanner, component_indices in schema.items():
        for component_index in component_indices:
            try:
                reversed_schema[component_index].append(new_covered_spanner)
            except KeyError:
                reversed_schema[component_index] = [new_covered_spanner]

    # iterate components and add new components to new spanners
    for component_index, new_component in enumerate(
        iterationtools.iterate_components_in_expr(new_components)):
        try:
            new_covered_spanners = reversed_schema[component_index]
            for new_covered_spanner in new_covered_spanners:
                new_covered_spanner.append(new_component)
        except KeyError:
            pass

    # repeat as specified by input
    for i in range(n - 1):
        new_components += copy_components_and_fracture_crossing_spanners(components)

    # return new components
    return new_components
