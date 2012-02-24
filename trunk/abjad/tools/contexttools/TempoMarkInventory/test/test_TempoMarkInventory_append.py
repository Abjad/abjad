from abjad import *


def test_TempoMarkInventory_append_01():

    tempo_mark_inventory_1 = contexttools.TempoMarkInventory([((1, 8), 72)])
    tempo_mark_inventory_1.append(((1, 8), 84))
    tempo_mark_inventory_2 = contexttools.TempoMarkInventory([((1, 8), 72), ((1, 8), 84)])
    
    assert tempo_mark_inventory_1 == tempo_mark_inventory_2
