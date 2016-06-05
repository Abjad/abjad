# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_TempoInventory___format___01():

    tempo_inventory = indicatortools.TempoInventory([
        ((1, 4), 84, 'Allegro'),
        ])

    assert format(tempo_inventory) == stringtools.normalize(
        r'''
        indicatortools.TempoInventory(
            [
                indicatortools.Tempo(
                    reference_duration=durationtools.Duration(1, 4),
                    units_per_minute=84,
                    textual_indication='Allegro',
                    ),
                ]
            )
        ''',
        )
