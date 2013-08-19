# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def inventory_aggregate_subsets():
    '''Inventory aggregate subsets:

    ::

        >>> U_star = pitchtools.inventory_aggregate_subsets()
        >>> len(U_star)
        4096
        >>> for pcset in U_star[:20]:
        ...   pcset
        NumberedPitchClassSet([])
        NumberedPitchClassSet([0])
        NumberedPitchClassSet([1])
        NumberedPitchClassSet([0, 1])
        NumberedPitchClassSet([2])
        NumberedPitchClassSet([0, 2])
        NumberedPitchClassSet([1, 2])
        NumberedPitchClassSet([0, 1, 2])
        NumberedPitchClassSet([3])
        NumberedPitchClassSet([0, 3])
        NumberedPitchClassSet([1, 3])
        NumberedPitchClassSet([0, 1, 3])
        NumberedPitchClassSet([2, 3])
        NumberedPitchClassSet([0, 2, 3])
        NumberedPitchClassSet([1, 2, 3])
        NumberedPitchClassSet([0, 1, 2, 3])
        NumberedPitchClassSet([4])
        NumberedPitchClassSet([0, 4])
        NumberedPitchClassSet([1, 4])
        NumberedPitchClassSet([0, 1, 4])

    There are 4096 subsets of the aggregate.

    This is ``U*`` in [Morris 1987].

    Return list of numbered chromatic pitch-class sets.
    '''
    from abjad.tools import pitchtools

    def _helper(binary_string):
        result = zip(binary_string, range(len(binary_string)))
        result = [x[1] for x in result if x[0] == '1']
        return result

    result = []

    for x in range(4096):
        subset = ''.join(list(reversed(mathtools.integer_to_binary_string(x).zfill(12))))
        subset = _helper(subset)
        subset = pitchtools.NumberedPitchClassSet(subset)
        result.append(subset)

    return result
