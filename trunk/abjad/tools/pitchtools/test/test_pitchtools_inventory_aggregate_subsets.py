from abjad import *


def test_pitchtools_inventory_aggregate_subsets_01():

    U_star = pitchtools.inventory_aggregate_subsets()
    assert len(U_star) == 4096
    assert pitchtools.NumberedChromaticPitchClassSet([0, 1, 2]) in U_star
    assert pitchtools.NumberedChromaticPitchClassSet([1, 2, 3]) in U_star
    assert pitchtools.NumberedChromaticPitchClassSet([3, 4, 8, 9, 11]) in U_star
    assert pitchtools.NumberedChromaticPitchClassSet(range(12)) in U_star
