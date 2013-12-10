# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_TempoInventory___format___01():

    tempo_inventory = indicatortools.TempoInventory([
        ('Allegro', (1, 4), 84),
        ])

    assert systemtools.TestManager.compare(
        format(tempo_inventory),
        r'''
        indicatortools.TempoInventory(
            [
                indicatortools.Tempo(
                    'Allegro',
                    durationtools.Duration(1, 4),
                    84
                    ),
                ]
            )
        ''',
        )
