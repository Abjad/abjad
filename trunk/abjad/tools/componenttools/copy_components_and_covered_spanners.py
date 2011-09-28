from abjad.tools.componenttools._ignore_parentage_of_components import _ignore_parentage_of_components
from abjad.tools.componenttools._restore_parentage_to_components_by_receipt import _restore_parentage_to_components_by_receipt
from abjad.tools.marktools._reattach_blinded_marks_to_components_in_expr import _reattach_blinded_marks_to_components_in_expr
import copy


def copy_components_and_covered_spanners(components, n=1):
    r'''.. versionadded:: 1.1

    Clone `components` and covered spanners.

    The `components` must be thread-contiguous.

    Covered spanners are those spanners that cover `components`.

    The steps taken in this function are as follows.
    Withdraw `components` from crossing spanners.
    Preserve spanners that `components` cover.
    Deep copy `components`.
    Reapply crossing spanners to source `components`.
    Return copied components with covered spanners. ::

        abjad> voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> beam = spannertools.BeamSpanner(voice.leaves[:4])
        abjad> f(voice)
        \new Voice {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                \time 2/8
                e'8
                f'8 ]
            }
            {
                \time 2/8
                g'8
                a'8
            }
        }

    ::

        abjad> result = componenttools.copy_components_and_covered_spanners(voice.leaves)
        abjad> result
        (Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8"))

    ::

        abjad> new_voice = Voice(result)
        abjad> f(new_voice)
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
        }

    ::

        abjad> voice.leaves[0] is new_voice.leaves[0]
        False

    Clone `components` a total of `n` times. ::

        abjad> result = componenttools.copy_components_and_covered_spanners(voice.leaves[:2], n = 3)
        abjad> result
        (Note("c'8"), Note("d'8"), Note("c'8"), Note("d'8"), Note("c'8"), Note("d'8"))

    ::

        abjad> new_voice = Voice(result)
        abjad> f(new_voice)
        \new Voice {
            c'8
            d'8
            c'8
            d'8
            c'8
            d'8
        }

    .. versionchanged:: 2.0
        renamed ``clone.covered()`` to
        ``componenttools.copy_components_and_covered_spanners()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_components_and_covered_spanners()`` to
        ``componenttools.copy_components_and_covered_spanners()``.
    '''
    from abjad.tools import spannertools
    from abjad.tools import componenttools

    if n < 1:
        return []

    assert componenttools.all_are_thread_contiguous_components(components)

#   spanners = spannertools.get_spanners_that_cross_components(components)
#   for spanner in spanners:
#      spanner._block_all_components()
#
#   receipt = _ignore_parentage_of_components(components)
#
#   result = copy.deepcopy(components)
#   for component in result:
#      #component._update._mark_all_improper_parents_for_update()
#      component._mark_entire_score_tree_for_later_update('prolated')
#
#   _restore_parentage_to_components_by_receipt(receipt)
#
#   for spanner in spanners:
#      spanner._unblock_all_components()
#
#   for i in range(n - 1):
#      result += copy_components_and_covered_spanners(components)
#
#   _reattach_blinded_marks_to_components_in_expr(result)
#
#   return result

    # deep copy components
    new_components = copy.deepcopy(components)

    # make schema of spanners covered by components
    schema = spannertools.make_covered_spanner_schema(components)

    # copy spanners covered by components
    for covered_spanner, component_indices in schema.items():
        new_covered_spanner = copy.copy(covered_spanner)
        del(schema[covered_spanner])
        schema[new_covered_spanner] = component_indices

    # reverse schema
    reversed_schema = {}
    for new_covered_spanner, component_indices in schema.items():
        for component_index in component_indices:
            try:
                reversed_schema[component_index].append(new_covered_spanner)
            except KeyError:
                reversed_schema[component_index] = [new_covered_spanner]

    # iterate components and add new components to new spanners
    for component_index, new_component in enumerate(
        componenttools.iterate_components_forward_in_expr(new_components)):
        try:
            new_covered_spanners = reversed_schema[component_index]
            for new_covered_spanner in new_covered_spanners:
                new_covered_spanner.append(new_component)
        except KeyError:
            pass

    # repeat as specified by input
    for i in range(n - 1):
        new_components += copy_components_and_covered_spanners(components)

    # return new components
    return new_components
