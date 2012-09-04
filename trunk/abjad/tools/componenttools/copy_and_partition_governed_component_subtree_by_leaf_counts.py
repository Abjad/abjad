from abjad.tools import mathtools
from abjad.tools import sequencetools


# TODO: Implement in-place containertools.partition_components_by_counts()
#       that doesn't climb to governor.
def copy_and_partition_governed_component_subtree_by_leaf_counts(container, leaf_counts):
    r'''.. versionadded:: 1.1

    Copy `container` and partition copy according to `leaf_counts`::

        >>> voice = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
        >>> beamtools.BeamSpanner(voice[0].leaves)
        BeamSpanner(c'8, d'8, e'8)
        >>> beamtools.BeamSpanner(voice[1].leaves)
        BeamSpanner(f'8, g'8, a'8)

    ::

        >>> f(voice)
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

        >>> result = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(
        ... voice, [1, 2, 3])

    ::

        >>> first, second, third = result

    ::

        >>> f(first)
        \new Voice {
            \times 2/3 {
                c'8 [ ]
            }
        }

    ::

        >>> f(second)
        \new Voice {
            \times 2/3 {
                d'8 [
                e'8 ]
            }
        }

    ::

        >>> f(third)
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
    from abjad.tools import componenttools
    from abjad.tools import containertools

    assert isinstance(container, containertools.Container)
    assert all([isinstance(x, int) for x in leaf_counts])

    result = []
    sums = mathtools.cumulative_sums_zero(leaf_counts)
    for start, stop in sequencetools.iterate_sequence_pairwise_strict(sums):
        result.append(componenttools.copy_governed_component_subtree_by_leaf_range(container, start, stop))
    return result
