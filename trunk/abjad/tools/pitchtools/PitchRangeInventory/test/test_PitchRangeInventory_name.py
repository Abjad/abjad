from abjad import *
import py


def test_PitchRangeInventory_name_01():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]'])
    assert inventory.name is None

    inventory.name = 'blue inventory'
    assert inventory.name == 'blue inventory'


def test_PitchRangeInventory_name_02():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]'])
    assert py.test.raises(Exception, 'inventory.name = 99')
