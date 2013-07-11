def attach_tie_spanner_to_leaf_pair(left_leaf, right_leaf):
    r'''Attach tie spanner to `left_leaf` and `right_leaf`:

    ::

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

        >>> tietools.attach_tie_spanner_to_leaf_pair(staff[1], staff[2])

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
    '''
    from abjad.tools import leaftools
    from abjad.tools import spannertools
    from abjad.tools import tietools

    # check input
    assert isinstance(left_leaf, leaftools.Leaf)
    assert isinstance(right_leaf, leaftools.Leaf)
    
    # make spanner classes filter
    spanner_classes = (tietools.TieSpanner, )

    # do nothing if leaves are already tied
    if left_leaf.get_tie_chain() == right_leaf.get_tie_chain():
        return

    # do nothing if leaves are already effectively tied 
    # because of parents somewhere in score tree
    left_parent_ties = left_leaf.parentage._get_spanners(spanner_classes)
    right_parent_ties = right_leaf.parentage._get_spanners(spanner_classes)
    shared_parent_ties = set(left_parent_ties) & set(right_parent_ties)
    if shared_parent_ties:
        return

    # get any left tie spanner
    try:
        left_tie_spanner = \
            spannertools.get_the_only_spanner_attached_to_component(
            left_leaf, spanner_classes=spanner_classes)
    except MissingSpannerError:
        left_tie_spanner = None

    # get any right tie spanner
    try:
        right_tie_spanner = \
            spannertools.get_the_only_spanner_attached_to_component(
            right_leaf, spanner_classes=spanner_classes)
    except MissingSpannerError:
        right_tie_spanner = None

    # fuse or apply tie spanner as appropriate
    if left_tie_spanner is not None and right_tie_spanner is not None:
        left_tie_spanner.fuse(right_tie_spanner)
    elif left_tie_spanner is not None and right_tie_spanner is None:
        left_tie_spanner.append(right_leaf)
    elif left_tie_spanner is None and right_tie_spanner is not None:
        right_tie_spanner.append_left(left_leaf)
    elif left_tie_spanner is None and right_tie_spanner is None:
        tietools.TieSpanner([left_leaf, right_leaf])
