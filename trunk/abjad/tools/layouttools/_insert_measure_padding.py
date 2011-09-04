from abjad.tools import durationtools
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools.resttools.Rest import Rest
from abjad.tools.skiptools.Skip import Skip


def _insert_measure_padding(expr, front, back, klass, splice = False):
    r'''.. versionadded:: 2.0

    Generalizes measuretools.pad_measures_in_expr_with_rests() and
    measuretools.pad_measures_in_expr_with_skips().
    '''
    from abjad.tools import componenttools
    from abjad.tools import measuretools

    if not isinstance(front, (durationtools.Duration, type(None))):
        raise ValueError

    if not isinstance(back, (durationtools.Duration, type(None))):
        raise ValueError

    if not isinstance(klass, (Rest, Skip)):
        raise TypeError

    #root = expr[0]._parentage.root
    root = componenttools.component_to_score_root(expr[0])

    # forbid updates because
    # componenttools.extend_in_parent_of_component_and_grow_spanners() and
    # componenttools.extend_left_in_parent_of_component_and_grow_spanners()
    # call self._offset.stop  #
    #root._update._forbid_component_update()
    root._update_prolated_offset_values_of_entire_score_tree_if_necessary()
    root._forbid_component_update()

    for measure in measuretools.iterate_measures_forward_in_expr(expr):
        if front is not None:
            start_components = measure._navigator._contemporaneous_start_contents
            start_leaves = [x for x in start_components if isinstance(x, _Leaf)]
            for start_leaf in start_leaves:
                if splice:
                    componenttools.extend_left_in_parent_of_component_and_grow_spanners(
                        start_leaf, [klass.__class__(front)])
                else:
                    componenttools.extend_left_in_parent_of_component_and_do_not_grow_spanners(
                        start_leaf, [klass.__class__(front)])
        if back is not None:
            stop_components = measure._navigator._contemporaneous_stop_contents
            stop_leaves = [x for x in stop_components if isinstance(x, _Leaf)]
            for stop_leaf in stop_leaves:
                if splice:
                    componenttools.extend_in_parent_of_component_and_grow_spanners(
                        stop_leaf, [klass.__class__(back)])
                else:
                    componenttools.extend_in_parent_of_component_and_do_not_grow_spanners(
                        stop_leaf, [klass.__class__(back)])

    # allow updates after all calls to spanner-growing functions are done #
    #root._update._allow_component_update()
    root._mark_entire_score_tree_for_later_update('prolated')
    root._allow_component_update()
