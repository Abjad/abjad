from abjad.tools.componenttools._Component import _Component
from abjad.tools.spannertools.get_spanners_attached_to_any_improper_child_of_component import get_spanners_attached_to_any_improper_child_of_component


def get_spanners_that_dominate_component_pair(left, right):
    '''Return Python list of (spanner, index) pairs.
    'left' must be either an Abjad component or None.
    'right' must be either an Abjad component or None.

    If both 'left' and 'right' are components,
    then 'left' and 'right' must be thread-contiguous.

    This is a special version of spannertools.get_spanners_that_dominate_components().
    This version is useful for finding spanners that dominant
    a zero-length 'crack' between components, as in t[2:2].

    .. versionchanged:: 2.0
        renamed ``spannertools.get_dominant_between()`` to
        ``spannertools.get_spanners_that_dominate_component_pair()``.
    '''
    from abjad.tools import componenttools

    if left is None or right is None:
        return set([])

    assert componenttools.all_are_thread_contiguous_components([left, right])

    #dominant_spanners = left.spanners.contained & right.spanners.contained
    left_contained = get_spanners_attached_to_any_improper_child_of_component(left)
    right_contained = get_spanners_attached_to_any_improper_child_of_component(right)
    dominant_spanners = left_contained & right_contained
    components_after_gap = right._navigator._contemporaneous_start_components

    receipt = set([])
    for spanner in dominant_spanners:
        for component in components_after_gap:
            if component in spanner:
                index = spanner.index(component)
                receipt.add((spanner, index))
                continue

    return receipt
