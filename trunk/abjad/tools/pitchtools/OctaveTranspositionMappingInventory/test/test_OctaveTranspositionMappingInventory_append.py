from abjad import *


def test_OctaveTranspositionMappingInventory_append_01():
    '''Append named item.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory()
    assert repr(inventory) == 'OctaveTranspositionMappingInventory([])'

    mapping = pitchtools.OctaveTranspositionMapping(name='foo')
    inventory.append(mapping)
    assert repr(inventory) == \
        "OctaveTranspositionMappingInventory([OctaveTranspositionMapping([], name='foo')])"
