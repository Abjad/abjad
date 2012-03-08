from abjad import *
import py


def test_PitchRangeInventory_inventory_name_01():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]'])
    assert inventory.inventory_name is None

    inventory.inventory_name = 'blue inventory'
    assert inventory.inventory_name == 'blue inventory'


def test_PitchRangeInventory_inventory_name_02():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]'])
    assert py.test.raises(Exception, 'inventory.inventory_name = 99')
