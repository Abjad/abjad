from abjad import *


def test_TempoMarkInventory__repr_with_tools_package_01():

    tempo_mark_inventory = contexttools.TempoMarkInventory([('Allegro', (1, 4), 84)])

    assert tempo_mark_inventory._repr_with_tools_package == \
        "contexttools.TempoMarkInventory([contexttools.TempoMark('Allegro', durationtools.Duration(1, 4), 84)])"
