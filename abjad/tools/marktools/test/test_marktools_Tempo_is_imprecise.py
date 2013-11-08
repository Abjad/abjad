# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Tempo_is_imprecise_01( ):
    r'''Tempo mark is imprecise if either duration or units_per_minute is None,
    or if units_per_minute is a tuple representing a tempo range.
    '''

    assert not Tempo(Duration(1, 4), 60).is_imprecise
    assert not Tempo('Langsam', 4, 60).is_imprecise
    assert Tempo('Langsam').is_imprecise
    assert Tempo('Langsam', 4, (35, 50)).is_imprecise
    assert Tempo(Duration(1, 4), (35, 50)).is_imprecise
