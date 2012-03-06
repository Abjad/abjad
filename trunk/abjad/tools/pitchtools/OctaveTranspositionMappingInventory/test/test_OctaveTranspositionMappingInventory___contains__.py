from abjad import *


def test_OctaveTranspositionMappingInventory___contains___01():
    '''Work with mappings.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory([[('[A0, C8]', -18)]])
    assert pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)]) in inventory


def test_OctaveTranspositionMappingInventory___contains___02():
    '''Work with mapping tokens.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory([[('[A0, C8]', -18)]])
    assert [('[A0, C8]', -18)] in inventory
