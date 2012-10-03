from abjad.tools import leaftools
from abjad.tools import spannertools


def apply_tie_spanner_to_leaf_pair(left, right):
    r'''Apply tie spanner to `left` leaf and `right` leaf::

        >>> staff = Staff("c'8 ~ c' c' c'")

    ::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'8
            c'8
            c'8
        }

    ::

        >>> tietools.apply_tie_spanner_to_leaf_pair(staff[1], staff[2])

    ::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8
            c'8
        }

    Handle existing tie spanners intelligently.

    Return none.

    .. versionchanged:: 2.0
        renamed ``tietools.span_leaf_pair()`` to
        ``tietools.apply_tie_spanner_to_leaf_pair()``.
    '''
    from abjad.tools import tietools

    # check input
    assert isinstance(left, leaftools.Leaf)
    assert isinstance(right, leaftools.Leaf)

    # do nothing if leaves are already tied
    if tietools.are_components_in_same_tie_spanner([left, right]):
        return

    # do nothing if leaves are already effectively tied because of parents somewhere in score tree
    left_parent_ties = spannertools.get_spanners_attached_to_any_proper_parent_of_component(
        left, klass=tietools.TieSpanner)
    right_parent_ties = spannertools.get_spanners_attached_to_any_proper_parent_of_component(
        right, klass=tietools.TieSpanner)
    shared_parent_ties = set(left_parent_ties) & set(right_parent_ties)
    if shared_parent_ties:
        return

    # get any left tie spanner
    try:
        left_tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
            left, tietools.TieSpanner)
    except MissingSpannerError:
        left_tie_spanner = None
    
    # get any right tie spanner
    try:
        right_tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
            right, tietools.TieSpanner)
    except MissingSpannerError:
        right_tie_spanner = None

    # fuse or apply tie spanner as appropriate
    if left_tie_spanner is not None and right_tie_spanner is not None:
        left_tie_spanner.fuse(right_tie_spanner)
    elif left_tie_spanner is not None and right_tie_spanner is None:
        left_tie_spanner.append(right)
    elif left_tie_spanner is None and right_tie_spanner is not None:
        right_tie_spanner.append_left(left)
    elif left_tie_spanner is None and right_tie_spanner is None:
        tietools.TieSpanner([left, right])
