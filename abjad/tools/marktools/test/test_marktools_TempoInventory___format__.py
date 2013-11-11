# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoInventory___format___01():

    tempo_mark_inventory = marktools.TempoInventory(
        [('Allegro', (1, 4), 84)])

    assert systemtools.TestManager.compare(
        format(tempo_mark_inventory),
        r'''
        marktools.TempoInventory([
            marktools.Tempo(
                'Allegro',
                durationtools.Duration(1, 4),
                84
                ),
            ])
        ''',
        )
