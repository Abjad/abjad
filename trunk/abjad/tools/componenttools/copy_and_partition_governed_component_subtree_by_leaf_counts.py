from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.sequencetools import iterate_sequence_pairwise_strict


# TODO: Implement in-place containertools.partition_components_by_counts() #
# that doesn't climb to governor #

def copy_and_partition_governed_component_subtree_by_leaf_counts(container, leaf_counts):
    r'''.. versionadded:: 1.1

    Copy `container` and partition copy according to `leaf_counts`::

        abjad> voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
        abjad> spannertools.BeamSpanner(voice[0].leaves)
        BeamSpanner(c'8, c'8, c'8)
        abjad> spannertools.BeamSpanner(voice[1].leaves)
        BeamSpanner(c'8, c'8, c'8)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> f(voice)
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                f'8 [
                g'8
                a'8 ]
            }
        }

    ::

        abjad> first, second, third = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(voice, [1, 2, 3])

    ::

        abjad> f(first)
        \new Voice {
            \times 2/3 {
                c'8 [ ]
            }
        }

    ::

        abjad> f(second)
        \new Voice {
            \times 2/3 {
                d'8 [
                e'8 ]
            }
        }

    ::

        abjad> f(third)
        \new Voice {
            \times 2/3 {
                f'8 [
                g'8
                a'8 ]
            }
        }

    Set `leaf_counts` to an iterable of zero or more positive integers.

    Return a list of parts equal in length to that of `leaf_counts`.

    .. versionchanged:: 2.0
        renamed ``clonewp.by_leaf_counts_with_parentage()`` to
        ``componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts()``.
    '''
    from abjad.tools.containertools.Container import Container
    from abjad.tools.componenttools.copy_governed_component_subtree_by_leaf_range import copy_governed_component_subtree_by_leaf_range

    assert isinstance(container, Container)
    assert all([isinstance(x, int) for x in leaf_counts])

    result = []
    sums = cumulative_sums_zero(leaf_counts)
    for start, stop in iterate_sequence_pairwise_strict(sums):
        result.append(copy_governed_component_subtree_by_leaf_range(container, start, stop))
    return result
