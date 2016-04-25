# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_ClefInventory___contains___01():

    inventory = indicatortools.ClefInventory(['treble', 'bass'])

    assert 'treble' in inventory
    assert Clef('treble') in inventory

    assert 'alto' not in inventory
    assert Clef('alto') not in inventory
