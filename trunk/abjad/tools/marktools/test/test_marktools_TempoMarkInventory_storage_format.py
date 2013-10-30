# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoMarkInventory_storage_format_01():

    tempo_mark_inventory = marktools.TempoMarkInventory(
        [('Allegro', (1, 4), 84)])

    assert testtools.compare(
        tempo_mark_inventory.storage_format,
        r'''
        marktools.TempoMarkInventory([
            marktools.TempoMark(
                'Allegro',
                durationtools.Duration(1, 4),
                84
                )
            ])
        ''',
        )
