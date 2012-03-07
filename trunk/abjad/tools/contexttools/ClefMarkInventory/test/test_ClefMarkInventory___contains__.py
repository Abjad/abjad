from abjad import *


def test_ClefMarkInventory___contains___01():

    inventory = contexttools.ClefMarkInventory(['treble', 'bass'])

    assert 'treble' in inventory
    assert contexttools.ClefMark('treble') in inventory

    assert 'alto' not in inventory
    assert contexttools.ClefMark('alto') not in inventory
