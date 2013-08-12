# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools import mutate


# TODO: bind to GovernorSelection?
#       it might make sense to force the composer to select
#       from `component` up to the governor of component;
#       that operation would return a GovernorSelection;
#       this method could be bound to GovernorSelection.
def copy_governed_component_subtree_by_leaf_range(
    component, start=0, stop=None):
    r'''Copy governed `component` subtree by leaf range.

    Governed subtree means `component` together with children of `component`.

    Leaf range refers to the sequential parentage of `component` 
    from `start` leaf index to `stop` leaf index:

    ::

        >>> voice = Voice(r"\times 2/3 { c'4 d'4 e'4 }")
        >>> voice.append(r"\times 2/3 { f'4 g'4 a'4 }")
        >>> staff = Staff([voice])

    ::

        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \new Voice {
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }
                \times 2/3 {
                    f'4
                    g'4
                    a'4
                }
            }
        }

    ::

        >>> result = \
        ...     componenttools.copy_governed_component_subtree_by_leaf_range(
        ...     staff, 1, 5)

    ::

        >>> result
        Staff{1}

    ::

        >>> show(result) # doctest: +SKIP

    ..  doctest::

        >>> f(result)
        \new Staff {
            \new Voice {
                \times 2/3 {
                    d'4
                    e'4
                }
                \times 2/3 {
                    f'4
                    g'4
                }
            }
        }

    Copy sequential containers in leaves' parentage up to
    the first simultaneous container in leaves' parentage.

    Trim and shrink copied containers as necessary.

    Copy all leaves from `start` forward when `stop` is none.

    Return new components.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    # trivial leaf lcopy
    if isinstance(component, leaftools.Leaf):
        result = mutate(leaf).copy_and_fracture_crossing_spanners()

    # copy leaves from sequential containers only
    if component.is_simultaneous:
        raise Exception('can not copy from simultaneous container.')

    # assert valid start and stop
    leaves = component.select_leaves()
    assert start <= len(leaves)
    if stop is None:
        stop = len(leaves)
    assert start < stop

    # new: find start and stop leaves in component
    start_leaf_in_component = leaves[start]
    stop_leaf_in_component = leaves[stop - 1]

    # get governor
    parentage = leaves[start]._select_parentage(include_self=True)
    governor = parentage._get_governor()

    # find start and stop leaves in governor
    governor_leaves = list(governor.select_leaves())
    for i, x in enumerate(governor_leaves):
        if x is start_leaf_in_component:
            start_index_in_governor = i
    for i, x in enumerate(governor_leaves):
        if x is stop_leaf_in_component:
            stop_index_in_governor = i

    # copy governor
    governor_copy = mutate(governor).copy_and_fracture_crossing_spanners()
    copy_leaves = governor_copy.select_leaves()

    # find start and stop leaves in copy of governor
    start_leaf = copy_leaves[start_index_in_governor]
    stop_leaf = copy_leaves[stop_index_in_governor]

    # trim governor copy forwards from first leaf
    _found_start_leaf = False

    while not _found_start_leaf:
        leaf = iterationtools.iterate_leaves_in_expr(governor_copy).next()
        if leaf is start_leaf:
            _found_start_leaf = True
        else:
            leaftools.remove_leaf_and_shrink_durated_parent_containers(leaf)

    # trim governor copy backwards from last leaf
    _found_stop_leaf = False

    while not _found_stop_leaf:
        reverse_iterator = iterationtools.iterate_leaves_in_expr(
            governor_copy, reverse=True)
        leaf = reverse_iterator.next()
        if leaf is stop_leaf:
            _found_stop_leaf = True
        else:
            leaftools.remove_leaf_and_shrink_durated_parent_containers(leaf)

    # return trimmed governor copy
    return governor_copy
    new_leaf = mutate(leaf).copy_and_fracture_crossing_spanners()
