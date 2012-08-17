from abjad.tools import mathtools
import copy


def partition_sequence_by_backgrounded_weights(sequence, weights):
    r'''.. versionadded:: 2.9

    Partition `sequence` by backgrounded `weights`::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.partition_sequence_by_backgrounded_weights(
        ...     [-5, -15, -10], [20, 10])
        [[-5, -15], [-10]]

    Further examples::

        >>> sequencetools.partition_sequence_by_backgrounded_weights(
        ...     [-5, -15, -10], [5, 5, 5, 5, 5, 5])
        [[-5], [-15], [], [], [-10], []]

    ::

        >>> sequencetools.partition_sequence_by_backgrounded_weights(
        ...     [-5, -15, -10], [1, 29])
        [[-5], [-15, -10]]

    ::

        >>> sequencetools.partition_sequence_by_backgrounded_weights(
        ...     [-5, -15, -10], [2, 28])
        [[-5], [-15, -10]]

    ::

        >>> sequencetools.partition_sequence_by_backgrounded_weights(
        ...     [-5, -15, -10], [1, 1, 1, 1, 1, 25])
        [[-5], [], [], [], [], [-15, -10]]

    The term `backgrounded` is a short-hand concocted specifically 
    for this function; rely on the formal definition to understand 
    the function actually does.

    Input constraint: the weight of `sequence` must equal the weight 
    of `weights` exactly.

    The signs of the elements in `sequence` are ignored.

    Formal definition: partition `sequence` into `parts` such that 
    (1.) the length of `parts` equals the length of `weights`; 
    (2.) the elements in `sequence` appear in order in `parts`; and
    (3.) some final condition that is difficult to formalize.

    Notionally what's going on here is that the elements of `weights` 
    are acting as a list of successive time intervals into which the 
    elements of `sequence` are being fit in accordance with the start 
    offset of each `sequence` element.

    The function models the grouping together of successive timespans 
    according to which of an underlying sequence of time intervals 
    it is in which each time span begins.

    Note that, for any input to this function, the flattened output 
    of this function always equals `sequence` exactly.

    Note too that while `partition` is being used here in the sense of 
    the other partitioning functions in the API, the distinguishing feature 
    is this funciton is its ability to produce empty lists as output.

    Return list of `sequence` objects.
    '''
    from abjad.tools import sequencetools

    assert all([0 < x for x in weights])
    assert mathtools.weight(sequence) == mathtools.weight(weights)

    start_offsets = mathtools.cumulative_sums_zero([abs(x) for x in sequence])[:-1]
    indicator = zip(start_offsets, sequence)

    result = []
    for interval_start, interval_stop in mathtools.cumulative_sums_zero_pairwise(weights):
        part = []
        for pair in indicator[:]:
            if interval_start <= pair[0] < interval_stop:
                part.append(pair[1])
                indicator.remove(pair)
        result.append(part)

    return result
