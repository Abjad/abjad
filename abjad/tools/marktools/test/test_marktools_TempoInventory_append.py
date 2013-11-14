# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoInventory_append_01():

    tempo_inventory_1 = marktools.TempoInventory([((1, 8), 72)])
    tempo_inventory_1.append(((1, 8), 84))
    tempo_inventory_2 = marktools.TempoInventory([((1, 8), 72), ((1, 8), 84)])

    assert tempo_inventory_1 == tempo_inventory_2
