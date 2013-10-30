# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_ClefMarkInventory___contains___01():

    inventory = marktools.ClefMarkInventory(['treble', 'bass'])

    assert 'treble' in inventory
    assert marktools.ClefMark('treble') in inventory

    assert 'alto' not in inventory
    assert marktools.ClefMark('alto') not in inventory
