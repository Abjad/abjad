from abjad import *


def test_PitchRangeInventory__tools_package_qualified_repr_pieces_01():

    inventory = pitchtools.PitchRangeInventory(['[C3, C6]', '[C4, C6]'])

    r'''
    pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C3, C6]'),
        pitchtools.PitchRange('[C4, C6]')
    ])
    '''

    assert '\n'.join(inventory._tools_package_qualified_repr_pieces) == "pitchtools.PitchRangeInventory([\n\tpitchtools.PitchRange('[C3, C6]'),\n\tpitchtools.PitchRange('[C4, C6]')\n])"
