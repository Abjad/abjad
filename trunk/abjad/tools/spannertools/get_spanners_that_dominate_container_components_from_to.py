from abjad.tools.spannertools.get_spanners_that_dominate_component_pair import get_spanners_that_dominate_component_pair
from abjad.tools.spannertools.get_spanners_that_dominate_components import get_spanners_that_dominate_components


def get_spanners_that_dominate_container_components_from_to(container, start, stop):
    '''Return Python list of (spanner, index) pairs.
    Each spanner dominates the components specified by slice
    with start index 'start' and stop index 'stop'.
    Generalization of dominant spanner-finding functions for slices.
    This exists for slices like t[2:2] that are empty lists.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_dominant_slice()`` to
        ``spannertools.get_spanners_that_dominate_container_components_from_to()``.
    '''

    from abjad.tools.containertools.Container import Container
    if not isinstance(container, Container):
        raise TypeError('Must be Abjad container.')

    if start == stop:
        if start == 0:
            left = None
        else:
            left = container[start - 1]
        if len(container) <= stop:
            right = None
        else:
            right = container[stop]
        spanners_receipt = get_spanners_that_dominate_component_pair(left, right)
    else:
        spanners_receipt = get_spanners_that_dominate_components(container[start:stop])

    return spanners_receipt
