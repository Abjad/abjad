from abjad import *


def test_PitchRangeInventory___contains___01():

    pitch_range_inventory = pitchtools.PitchRangeInventory(['[C3, C6]', '[C4, C6]'])

    assert '[C3, C6]' in pitch_range_inventory
    assert (-12, 24) in pitch_range_inventory
    assert (-39, 48) not in pitch_range_inventory
