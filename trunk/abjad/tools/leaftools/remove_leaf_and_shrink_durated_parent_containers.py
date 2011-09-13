from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.componenttools.get_proper_parentage_of_component import get_proper_parentage_of_component
from abjad.tools.componenttools.remove_component_subtree_from_score_and_spanners import remove_component_subtree_from_score_and_spanners


def remove_leaf_and_shrink_durated_parent_containers(leaf):
    r'''.. versionadded:: 1.1

    Remove `leaf` and shrink durated parent containers::

        abjad> measure = Measure((4, 8), tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(measure)
        abjad> spannertools.BeamSpanner(measure.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8, g'8, a'8)
        abjad> f(measure)
        {
            \time 4/8
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8 ]
            }
        }

    ::

        abjad> leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.leaves[0])

    ::

        abjad> f(measure)
        {
            \time 5/12
            \scaleDurations #'(2 . 3) {
                {
                    d'8 [
                    e'8
                }
                {
                    f'8
                    g'8
                    a'8 ]
                }
            }
        }

    Return none.
    '''
    from abjad.tools import contexttools
    from abjad.tools.measuretools.Measure import Measure
    from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet

    prolated_leaf_duration = leaf.prolated_duration
    prolations = leaf._prolations
    cur_prolation, i = durationtools.Duration(1), 0
    parent = leaf._parentage.parent

    while parent is not None and not parent.is_parallel:
        cur_prolation *= prolations[i]
        if isinstance(parent, FixedDurationTuplet):
            candidate_new_parent_dur = parent.target_duration - cur_prolation * leaf.written_duration
            if durationtools.Duration(0) < candidate_new_parent_dur:
                parent.target_duration = candidate_new_parent_dur
        elif isinstance(parent, Measure):
            parent_time_signature = contexttools.get_time_signature_mark_attached_to_component(parent)
            old_denominator = parent_time_signature.denominator
            naive_meter = parent_time_signature.duration - prolated_leaf_duration
            better_meter = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                naive_meter, old_denominator)
            better_meter = contexttools.TimeSignatureMark(better_meter)
            contexttools.detach_time_signature_marks_attached_to_component(parent)
            better_meter.attach(parent)
            parent_time_signature = contexttools.get_time_signature_mark_attached_to_component(parent)
            new_denominator = parent_time_signature.denominator

            old_prolation = durationtools.positive_integer_to_implied_prolation_multipler(old_denominator)
            new_prolation = durationtools.positive_integer_to_implied_prolation_multipler(new_denominator)
            adjusted_prolation = old_prolation / new_prolation
            for x in parent:
                if isinstance(x, FixedDurationTuplet):
                    x.target_duration *= adjusted_prolation
                else:
                    if adjusted_prolation != 1:
                        new_target = x.preprolated_duration * adjusted_prolation
                        FixedDurationTuplet(new_target, [x])
        parent = parent._parentage.parent
        i += 1
    parentage = get_proper_parentage_of_component(leaf)
    remove_component_subtree_from_score_and_spanners([leaf])
    for x in parentage:
        if not len(x):
            remove_component_subtree_from_score_and_spanners([x])
        else:
            break
