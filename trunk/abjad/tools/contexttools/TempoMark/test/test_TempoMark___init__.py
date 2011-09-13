from abjad import *


def test_TempoMark___init___01():
    '''Init tempo mark with integer-valued mark.'''

    t = contexttools.TempoMark(Duration(3, 32), 52)
    assert t.format == '\\tempo 16.=52'


def test_TempoMark___init___02():
    '''Init tempo mark with float-valued mark.'''

    t = contexttools.TempoMark(Duration(3, 32), 52.5)
    assert t.format == '\\tempo 16.=52.5'


def test_TempoMark___init___03():
    '''Init tempo mark from tempo mark.'''

    t = contexttools.TempoMark(Duration(3, 32), 52)
    new = contexttools.TempoMark(t)

    assert t == new
    assert t is not new

    assert t.duration == new.duration
    assert t.duration is not new.duration


def test_TempoMark___init___04():
    '''Init tempo mark from integer pair.'''

    t = contexttools.TempoMark((3, 32), 52.5)
    assert t.format == '\\tempo 16.=52.5'
