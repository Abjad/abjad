# -*- encoding: utf-8 -*-
import copy


def copy_components_and_fracture_crossing_spanners(components, n=1):
    r'''Copy `components` and fracture crossing spanners.

    The `components` must be thread-contiguous.

    The steps this function takes are as follows.
    Deep copy `components`.
    Deep copy spanners that attach to any component in `components`.
    Fracture spanners that attach to components not in `components`.
    Return Python list of copied components.

    ::

        >>> voice = Voice(r"abj: | 2/8 c'8 [ d'8 || 2/8 e'8 f'8 ] |")
        >>> voice.append(r"abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    ::

        >>> show(voice) # doctest: +SKIP

    ::

        >>> result = \
        ...     componenttools.copy_components_and_fracture_crossing_spanners(
        ...     voice.select_leaves()[2:4])
        >>> new_voice = Voice(result)

    ::

        >>> voice.select_leaves()[2] is new_voice.select_leaves()[0]
        False

    ::

        >>> show(new_voice) # doctest: +SKIP

    Copy `components` a total of `n` times:
    
    ::

        >>> result = \
        ...     componenttools.copy_components_and_fracture_crossing_spanners(
        ...     voice.select_leaves()[2:4], n=4)
        >>> new_voice = Voice(result)

    ::

        >>> show(new_voice) # doctest: +SKIP

    Return new components.
    '''
    from abjad.tools import spannertools
    from abjad.tools import componenttools
    from abjad.tools import iterationtools


    # check input
    assert componenttools.all_are_thread_contiguous_components(components), \
        repr(components)

    # return empty list when nothing to copy
    if n < 1:
        return []

    new_components = [
        component._copy_with_children_and_marks_but_without_spanners() 
        for component in components]
    new_components = type(components)(new_components)

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
        new_components += copy_components_and_fracture_crossing_spanners(
            components)

    # return new components
    return new_components
