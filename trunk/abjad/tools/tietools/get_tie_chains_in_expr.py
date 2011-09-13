from abjad.exceptions import MissingSpannerError
from abjad.tools import componenttools
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner


def get_tie_chains_in_expr(components):
    '''This function returns all tie chains in components. A tie chain may
    not encompass all the leaves spanned by its corresponding Tie spanner,
    but only those found in the given list. i.e. the function returns the
    intersection between all the leav es spanned by all tie spanners touching
    the components given and the leaves found in the given components list.

    .. versionchanged:: 2.0
        renamed ``tietools.get_tie_chains()`` to
        ``tietools.get_tie_chains_in_expr()``.
    '''
    from abjad.tools import leaftools

    assert componenttools.all_are_components(components)

    # collect tie spanners in components
    tie_spanners = []
    for component in components:
        spanners = spannertools.get_spanners_attached_to_component(component, TieSpanner)
        #if component.tie.spanned:
        if spanners:
            #spanner = component.tie.spanner
            spanner = spanners.pop()
            if not spanner in tie_spanners:
                #tie_spanners.append(component.tie.spanner)
                tie_spanners.append(spanner)

    # get leaves to fuse
    result = []
    #leaves_in_components = list(leaftools.iterate_leaves_forward_in_expr(components))
    leaves_in_components = set(leaftools.iterate_leaves_forward_in_expr(components))
    for spanner in tie_spanners:
        leaves_intersecting = []
        for leaf in spanner.leaves:
            if leaf in leaves_in_components:
                leaves_intersecting.append(leaf)
        result.append(tuple(leaves_intersecting))
    return result
