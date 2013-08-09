# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import mathtools


def pad_measures_in_expr(expr, front, back, pad_class, splice=False):
    r'''Pad measures in `expr`.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import resttools
    from abjad.tools import skiptools

    if not isinstance(front, (durationtools.Duration, type(None))):
        raise ValueError

    if not isinstance(back, (durationtools.Duration, type(None))):
        raise ValueError

    if not isinstance(pad_class, (resttools.Rest, skiptools.Skip)):
        raise TypeError

    root = expr[0]._select_parentage().root

    # forbid updates because self.splice() calls self.stop_offset
    #root._update._forbid_component_update()
    root._update_prolated_offset_values_of_entire_score_tree_if_necessary()
    root._forbid_component_update()

    for measure in iterationtools.iterate_measures_in_expr(expr):
        if front is not None:
            start_components = measure._select_descendants_starting_with()
            start_leaves = \
                [x for x in start_components if isinstance(x, leaftools.Leaf)]
            for start_leaf in start_leaves:
                if splice:
                    start_leaf.splice(
                        [pad_class.__class__(front)], 
                        direction=Left,
                        grow_spanners=True,
                        )
                else:
                    start_leaf.splice(
                        [pad_class.__class__(front)], 
                        direction=Left,
                        grow_spanners=False,
                        )
        if back is not None:
            stop_components = measure._select_descendants_stopping_with()
            stop_leaves = \
                [x for x in stop_components if isinstance(x, leaftools.Leaf)]
            for stop_leaf in stop_leaves:
                if splice:
                    stop_leaf.splice(
                        [pad_class.__class__(back)],
                        grow_spanners=True,
                        )
                else:
                    stop_leaf.splice(
                        [pad_class.__class__(back)],
                        grow_spanners=False,
                        )
        if front is not None or back is not None:
            new_duration = measure.get_duration()
            new_time_signature = mathtools.NonreducedFraction(new_duration)
            old_time_signature = measure._get_mark(
                contexttools.TimeSignatureMark)
            new_time_signature = new_time_signature.with_denominator(
                old_time_signature.denominator)
            new_time_signature = contexttools.TimeSignatureMark(
                new_time_signature)
            measure.select().detach_marks(contexttools.TimeSignatureMark)
            new_time_signature.attach(measure)

    # allow updates after all calls to spanner-growing functions are done
    #root._update._allow_component_update()
    root._mark_entire_score_tree_for_later_update('prolated')
    root._allow_component_update()
