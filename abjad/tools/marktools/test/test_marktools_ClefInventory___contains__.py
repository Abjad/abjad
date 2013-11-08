# -*- encoding: utf-8 -*-
from abjad import *


def test_ClefMarkInventory___contains___01():

    inventory = marktools.ClefMarkInventory(['treble', 'bass'])

    assert 'treble' in inventory
    assert Clef('treble') in inventory

    assert 'alto' not in inventory
    assert Clef('alto') not in inventory
