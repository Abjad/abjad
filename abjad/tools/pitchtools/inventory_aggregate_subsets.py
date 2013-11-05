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
        PitchClassSet([])
        PitchClassSet([0])
        PitchClassSet([1])
        PitchClassSet([0, 1])
        PitchClassSet([2])
        PitchClassSet([0, 2])
        PitchClassSet([1, 2])
        PitchClassSet([0, 1, 2])
        PitchClassSet([3])
        PitchClassSet([0, 3])
        PitchClassSet([1, 3])
        PitchClassSet([0, 1, 3])
        PitchClassSet([2, 3])
        PitchClassSet([0, 2, 3])
        PitchClassSet([1, 2, 3])
        PitchClassSet([0, 1, 2, 3])
        PitchClassSet([4])
        PitchClassSet([0, 4])
        PitchClassSet([1, 4])
        PitchClassSet([0, 1, 4])

    There are 4096 subsets of the aggregate.

    This is ``U*`` in [Morris 1987].

    Returns list of numbered pitch-class sets.
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
        subset = pitchtools.PitchClassSet(
            subset,
            item_class=pitchtools.NumberedPitchClass,
            )
        result.append(subset)

    return result
