from abjad import *


def test_TempoMark_units_per_minute_01():
    '''Tempo mark units per minute is read / write.
    '''

    tempo = contexttools.TempoMark(Duration(1, 8), 52)
    assert tempo.units_per_minute == 52

    tempo.units_per_minute = 56
    assert tempo.units_per_minute == 56
