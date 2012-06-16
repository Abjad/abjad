from abjad import *


def test_PitchRangeInventory_storage_format_01():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]', '[C4, D5]'])

    r'''
    pitchtools.PitchRangeInventory([
        pitchtools.PitchRange(
            '[A0, C8]'
            ),
        pitchtools.PitchRange(
            '[C4, D5]'
            )
        ])
    '''

    assert inventory.storage_format == "pitchtools.PitchRangeInventory([\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\tpitchtools.PitchRange(\n\t\t'[C4, D5]'\n\t\t)\n\t])"
