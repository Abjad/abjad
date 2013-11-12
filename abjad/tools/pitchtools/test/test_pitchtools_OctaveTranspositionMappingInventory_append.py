# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMappingInventory_append_01():
    r'''Append named item.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory()
    assert repr(inventory) == 'OctaveTranspositionMappingInventory([])'

    mapping = pitchtools.OctaveTranspositionMapping(custom_identifier='foo')
    inventory.append(mapping)
    assert repr(inventory) == \
        "OctaveTranspositionMappingInventory([OctaveTranspositionMapping([], custom_identifier='foo')])"
