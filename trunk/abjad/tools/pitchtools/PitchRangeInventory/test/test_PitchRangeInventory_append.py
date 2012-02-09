from abjad import *


def test_PitchRangeInventory_append_01():

    pitch_range_inventory_1 = pitchtools.PitchRangeInventory(['[A0, C8]'])
    pitch_range_inventory_1.append('[C3, F#5]')
    pitch_range_inventory_2 = pitchtools.PitchRangeInventory(['[A0, C8]', '[C3, F#5]'])

    assert pitch_range_inventory_1 == pitch_range_inventory_2
