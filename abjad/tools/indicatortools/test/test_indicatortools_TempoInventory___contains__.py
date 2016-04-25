# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_TempoInventory___contains___01():

    tempo_inventory = indicatortools.TempoInventory([
        (Duration(1, 8), 72),
        ((1, 8), 84, 'Allegro'),
        ])

    assert Tempo((1, 8), 72) in tempo_inventory
    assert ((1, 8), 72) in tempo_inventory
    assert (Duration(1, 8), 72) in tempo_inventory
    assert ((1, 8), 84, 'Allegro') in tempo_inventory
    assert ((1, 8), 96) not in tempo_inventory
