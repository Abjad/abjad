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
    from abjad.tools import tietools

    # check input
    assert isinstance(left_leaf, leaftools.Leaf)
    assert isinstance(right_leaf, leaftools.Leaf)
    
    # get tie chains
    left_tie_chain = left_leaf.get_tie_chain()
    right_tie_chain = right_leaf.get_tie_chain()

    # do nothing if leaves are already tied
    if left_tie_chain == right_tie_chain:
        return

    # TODO: use the following two lines
    #left_tie_spanner = left_tie_chain.tie_spanner
    #right_tie_spanner = right_tie_chain.tie_spanner

    # TODO: remove in favor of TieChain.tie_spanner property
    try:
        left_tie_spanner = left_leaf._get_spanner((tietools.TieSpanner,))
    except MissingSpannerError:
        left_tie_spanner = None

    # TODO: remove in favor of TieChain.tie_spanner property
    try:
        right_tie_spanner = right_leaf._get_spanner((tietools.TieSpanner,))
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
