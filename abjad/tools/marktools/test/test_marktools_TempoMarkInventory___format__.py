# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoMarkInventory___format___01():

    tempo_mark_inventory = marktools.TempoMarkInventory(
        [('Allegro', (1, 4), 84)])

    assert testtools.compare(
        format(tempo_mark_inventory),
        r'''
        marktools.TempoMarkInventory([
            marktools.TempoMark(
                'Allegro',
                durationtools.Duration(1, 4),
                84
                ),
            ])
        ''',
        )
