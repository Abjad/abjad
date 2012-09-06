from abjad.tools import mathtools


def merge_duration_sequences(*sequences):
    r'''.. versionadded: 2.10

    Merge duration `sequences`::

        >>> sequencetools.merge_duration_sequences([10, 10, 10], [7])
        [7, 3, 10, 10]

    Merge more duration sequences::

        >>> sequencetools.merge_duration_sequences([10, 10, 10], [10, 10])
        [10, 10, 10]

    The idea is that each sequence element represents a duration.

    Return list.
    '''
    from abjad.tools import sequencetools

    offset_lists = []
    for sequence in sequences:
        offset_list = mathtools.cumulative_sums(sequence)
        offset_lists.append(offset_list)

    all_offsets = sequencetools.join_subsequences(offset_lists)
    all_offsets = list(sorted(set(all_offsets))) 
    all_offsets.insert(0, 0)
    all_durations = mathtools.difference_series(all_offsets)

    return all_durations
