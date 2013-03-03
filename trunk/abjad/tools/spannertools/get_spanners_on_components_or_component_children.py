from abjad.tools import componenttools


def get_spanners_on_components_or_component_children(components):
    '''Return unordered set of all spanners attaching to any
    component in `components` or attaching to any of the children
    of any of the components in `components`.
    '''

    # check input
    assert componenttools.all_are_contiguous_components_in_same_thread(components)

    # accumulate spanners
    spanners = set([])
    for component in components:
        #for spanner in list(component.spanners._spanners):
        for spanner in component.spanners:
            spanners.update((spanner, ))

    # return spanners
    return spanners
