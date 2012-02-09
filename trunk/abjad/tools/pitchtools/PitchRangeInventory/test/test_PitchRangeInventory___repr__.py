from abjad import *
from abjad.tools.pitchtools import PitchRange


def test_PitchRangeInventory___repr___01():
    '''Pitch range inventory reprs evaluate.
    '''

    pitch_range_inventory_1 = pitchtools.PitchRangeInventory(['[A0, C8]', '[C3, F#5]'])
    pitch_range_inventory_2 = pitchtools.PitchRangeInventory(pitch_range_inventory_1)

    assert pitch_range_inventory_1 == pitch_range_inventory_2
