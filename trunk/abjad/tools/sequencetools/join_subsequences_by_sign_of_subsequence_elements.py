from abjad.tools.mathtools.get_shared_numeric_sign import get_shared_numeric_sign


def join_subsequences_by_sign_of_subsequence_elements(sequence):
    '''.. versionadded:: 1.1

    Join subsequences in `sequence` by sign::

        >>> sequence = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
        >>> sequencetools.join_subsequences_by_sign_of_subsequence_elements(sequence)
        [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]

    ::

        >>> sequence = [[1, 2], [], [], [3, 4, 5], [6, 7]]
        >>> sequencetools.join_subsequences_by_sign_of_subsequence_elements(sequence)
        [[1, 2], [], [3, 4, 5, 6, 7]]

    Return newly constructed list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.join_sublists_by_sign()`` to
        ``sequencetools.join_subsequences_by_sign_of_subsequence_elements()``.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    if not all([isinstance(x, list) for x in sequence]):
        raise TypeError

    if any([get_shared_numeric_sign(x) is None for x in sequence]):
        raise ValueError

    result = []

    for sublist in sequence:
        try:
            previous_sublist = result[-1]
            if get_shared_numeric_sign(previous_sublist) == get_shared_numeric_sign(sublist):
                previous_sublist.extend(sublist)
            else:
                result.append(sublist[:])
        except IndexError:
            result.append(sublist[:])

    return result
