# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo_is_imprecise_01( ):
    r'''Tempo is imprecise if either duration or units_per_minute is none,
    or if units_per_minute is a tuple representing a tempo range.
    '''

    assert not Tempo(Duration(1, 4), 60).is_imprecise
    assert not Tempo(4, 60, 'Langsam').is_imprecise
    assert Tempo(textual_indication='Langsam').is_imprecise
    assert Tempo(4, (35, 50), 'Langsam').is_imprecise
    assert Tempo(Duration(1, 4), (35, 50)).is_imprecise
