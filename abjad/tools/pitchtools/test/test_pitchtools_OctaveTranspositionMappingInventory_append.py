# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMappingInventory_append_01():
    r'''Append named item.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory()
    assert repr(inventory) == 'OctaveTranspositionMappingInventory([])'
