def copy_governed_component_subtree_by_leaf_range(component, start=0, stop=None):
    r'''.. versionadded:: 1.1

    Copy governed `component` subtree by leaf range.

    Governed subtree means `component` together with children of `component`.

    Leaf range refers to the sequential parentage of `component` from `start` leaf index
    to `stop` leaf index::

        >>> voice = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
        >>> t = Staff([voice])

    ::

        >>> f(t)
        \new Staff {
            \new Voice {
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
                \times 2/3 {
                    f'8
                    g'8
                    a'8
                }
            }
        }

    ::

        >>> u = componenttools.copy_governed_component_subtree_by_leaf_range(t, 1, 5)
        >>> f(u)
        \new Staff {
            \new Voice {
                \times 2/3 {
                    d'8
                    e'8
                }
                \times 2/3 {
                    f'8
                    g'8
                }
            }
        }

    Copy sequential containers in leaves' parentage up to
    the first parallel container in leaves' parentage.

    Trim and shrink copied containers as necessary.

    When `stop` is none copy all leaves from `start` forward.

    .. versionchanged:: 2.0
        renamed ``clonewp.by_leaf_range_with_parentage()`` to
        ``componenttools.copy_governed_component_subtree_by_leaf_range()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_governed_component_subtree_by_leaf_range()`` to
        ``componenttools.copy_governed_component_subtree_by_leaf_range()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    # trivial leaf lcopy
    if isinstance(component, leaftools.Leaf):
        return componenttools.copy_components_and_fracture_crossing_spanners([component])[0]

    # copy leaves from sequential containers only.
    if component.is_parallel:
        raise ContiguityError('can not lcopy leaves from parallel container.')

    # assert valid start and stop
    leaves = component.leaves
    assert start <= len(leaves)
    if stop is None:
        stop = len(leaves)
    assert start < stop

    # new: find start and stop leaves in component
    start_leaf_in_component = leaves[start]
    stop_leaf_in_component = leaves[stop - 1]

    # find governor
    governor = componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        leaves[start])

    # new: find start and stop leaves in governor
    governor_leaves = list(governor.leaves)
    #start_index_in_governor = governor_leaves.index(start_leaf_in_component)
    #stop_index_in_governor = governor_leaves.index(stop_leaf_in_component)
    for i, x in enumerate(governor_leaves):
        if x is start_leaf_in_component:
            start_index_in_governor = i
    for i, x in enumerate(governor_leaves):
        if x is stop_leaf_in_component:
            stop_index_in_governor = i

    # copy governor
    governor_copy = componenttools.copy_components_and_fracture_crossing_spanners([governor])[0]
    copy_leaves = governor_copy.leaves

    # new: find start and stop leaves in copy of governor
    start_leaf = copy_leaves[start_index_in_governor]
    stop_leaf = copy_leaves[stop_index_in_governor]

    # trim governor copy forwards from first leaf
    _found_start_leaf = False

    while not _found_start_leaf:
        leaf = iterationtools.iterate_leaves_in_expr(governor_copy).next()
        #if leaf == start_leaf:
        if leaf is start_leaf:
            _found_start_leaf = True
        else:
            leaftools.remove_leaf_and_shrink_durated_parent_containers(leaf)

    #print 'moved on to trimming backwards ...'

    # trim governor copy backwards from last leaf
    _found_stop_leaf = False

    while not _found_stop_leaf:
        leaf = iterationtools.iterate_leaves_in_expr(governor_copy, reverse=True).next()
        #if leaf == stop_leaf:
        if leaf is stop_leaf:
            _found_stop_leaf = True
        else:
            leaftools.remove_leaf_and_shrink_durated_parent_containers(leaf)

    # return trimmed governor copy
    return governor_copy
