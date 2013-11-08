# -*- encoding: utf-8 -*-
from abjad import *


def test_TempoMarkInventory___contains___01():

    tempo_mark_inventory = marktools.TempoInventory([(Duration(1, 8), 72), ('Allegro', (1, 8), 84)])

    assert Tempo((1, 8), 72) in tempo_mark_inventory
    assert ((1, 8), 72) in tempo_mark_inventory
    assert (Duration(1, 8), 72) in tempo_mark_inventory
    assert ('Allegro', (1, 8), 84) in tempo_mark_inventory
    assert ((1, 8), 96) not in tempo_mark_inventory
