from abjad import *


def test_OctaveTranspositionMapping_inventory_name_01():

    mapping = pitchtools.OctaveTranspositionMapping()
    assert mapping.inventory_name is None

    mapping.inventory_name = 'lower register mapping #2'
    assert mapping.inventory_name == 'lower register mapping #2'
