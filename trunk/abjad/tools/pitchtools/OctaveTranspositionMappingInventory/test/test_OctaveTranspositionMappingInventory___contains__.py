# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveTranspositionMappingInventory___contains___01():
    r'''Work with mappings.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory([[('[A0, C8]', -18)]])
    assert pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)]) in inventory


def test_OctaveTranspositionMappingInventory___contains___02():
    r'''Work with mapping tokens.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory([[('[A0, C8]', -18)]])
    assert [('[A0, C8]', -18)] in inventory
