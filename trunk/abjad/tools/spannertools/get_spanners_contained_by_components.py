# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_spanners_contained_by_components(components):
    r'''Return unordered set of spanners contained within
    any component in list of logical-voice-contiguous components.
    Getter for t.spanners.contained across logical-voice-contiguous components.
    '''
    from abjad.tools import spannertools

    assert componenttools.all_are_contiguous_components_in_same_logical_voice(components)

    result = set([])
    for component in components:
        result.update(
            spannertools.get_spanners_attached_to_any_improper_child_of_component(
                component))
    return result
