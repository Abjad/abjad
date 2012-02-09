from abjad import *


def test_TempoMark_duration_01():
    '''Duration of tempo mark is read / write.
    '''

    tempo = contexttools.TempoMark(Duration(1, 8), 52)
    assert tempo.duration == Duration(1, 8)

    tempo.duration = Duration(1, 4)
    assert tempo.duration == Duration(1, 4)

    tempo.duration = None
    assert tempo.duration is None
