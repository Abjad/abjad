# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import OctaveTranspositionMapping
from abjad.tools.pitchtools import OctaveTranspositionMappingInventory


def test_pitchtools_OctaveTranspositionMappingInventory___repr___01():

    inventory_1 = pitchtools.OctaveTranspositionMappingInventory([[('[A0, C8]', -18)]])
    inventory_2 = eval(repr(inventory_1))

    assert isinstance(inventory_1, pitchtools.OctaveTranspositionMappingInventory)
    assert isinstance(inventory_2, pitchtools.OctaveTranspositionMappingInventory)
    assert inventory_1 == inventory_2


def test_pitchtools_OctaveTranspositionMappingInventory___repr___02():
    r'''Kwargs appear in repr.
    '''

    inventory = pitchtools.OctaveTranspositionMappingInventory(
        [[('[A0, C8]', -18)]],
        custom_identifier='special inventory')

    assert repr(inventory) == "OctaveTranspositionMappingInventory([OctaveTranspositionMapping([('[A0, C8]', -18)])], custom_identifier='special inventory')"
