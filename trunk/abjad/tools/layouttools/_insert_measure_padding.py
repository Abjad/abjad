from abjad.tools import durationtools
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import resttools
from abjad.tools import skiptools


# TODO: make public and possibly improve function name
def _insert_measure_padding(expr, front, back, klass, splice=False):
    r'''.. versionadded:: 2.0

    Generalizes measuretools.pad_measures_in_expr_with_rests() and
    measuretools.pad_measures_in_expr_with_skips().
    '''

    if not isinstance(front, (durationtools.Duration, type(None))):
        raise ValueError

    if not isinstance(back, (durationtools.Duration, type(None))):
        raise ValueError

    if not isinstance(klass, (resttools.Rest, skiptools.Skip)):
        raise TypeError

    #root = expr[0]._parentage.root
    root = componenttools.component_to_score_root(expr[0])

    # forbid updates because
    # componenttools.extend_in_parent_of_component() and
    # componenttools.extend_left_in_parent_of_component()
    # call self.stop
    #root._update._forbid_component_update()
    root._update_prolated_offset_values_of_entire_score_tree_if_necessary()
    root._forbid_component_update()

    for measure in iterationtools.iterate_measures_in_expr(expr):
        if front is not None:
            start_components = componenttools.get_improper_descendents_of_component_that_start_with_component(
                measure)
            start_leaves = [x for x in start_components if isinstance(x, leaftools.Leaf)]
            for start_leaf in start_leaves:
                if splice:
                    componenttools.extend_left_in_parent_of_component(
                        start_leaf, [klass.__class__(front)], grow_spanners=True)
                else:
                    componenttools.extend_left_in_parent_of_component(
                        start_leaf, [klass.__class__(front)], grow_spanners=False)
        if back is not None:
            stop_components = componenttools.get_improper_descendents_of_component_that_stop_with_component(
                measure)
            stop_leaves = [x for x in stop_components if isinstance(x, leaftools.Leaf)]
            for stop_leaf in stop_leaves:
                if splice:
                    componenttools.extend_in_parent_of_component(
                        stop_leaf, [klass.__class__(back)], grow_spanners=True)
                else:
                    componenttools.extend_in_parent_of_component(
                        stop_leaf, [klass.__class__(back)], grow_spanners=False)

    # allow updates after all calls to spanner-growing functions are done #
    #root._update._allow_component_update()
    root._mark_entire_score_tree_for_later_update('prolated')
    root._allow_component_update()
