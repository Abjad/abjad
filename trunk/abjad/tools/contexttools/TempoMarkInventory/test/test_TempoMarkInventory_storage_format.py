from abjad import *


def test_TempoMarkInventory_storage_format_01():

    tempo_mark_inventory = contexttools.TempoMarkInventory([('Allegro', (1, 4), 84)])

    r'''
    contexttools.TempoMarkInventory([
        contexttools.TempoMark(
            'Allegro',
            durationtools.Duration(1, 4),
            84
            )
        ])
    '''

    assert tempo_mark_inventory.storage_format == "contexttools.TempoMarkInventory([\n\tcontexttools.TempoMark(\n\t\t'Allegro',\n\t\tdurationtools.Duration(1, 4),\n\t\t84\n\t\t)\n\t])"
