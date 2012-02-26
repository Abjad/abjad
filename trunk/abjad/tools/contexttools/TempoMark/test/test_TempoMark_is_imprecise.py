from abjad import *


def test_TempoMark_is_imprecise_01( ):
    '''Tempo mark is imprecise if either duration or units_per_minute is None,
    or if units_per_minute is a tuple representing a tempo range.
    '''

    assert not contexttools.TempoMark(Duration(1, 4), 60).is_imprecise
    assert not contexttools.TempoMark('Langsam', 4, 60).is_imprecise
    assert contexttools.TempoMark('Langsam').is_imprecise
    assert contexttools.TempoMark('Langsam', 4, (35, 50)).is_imprecise
    assert contexttools.TempoMark(Duration(1, 4), (35, 50)).is_imprecise
