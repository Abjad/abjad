# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoMark___init___01():
    r'''Init tempo mark with integer-valued mark.
    '''

    tempomark = marktools.TempoMark(Duration(3, 32), 52)
    assert format(tempomark) == '\\tempo 16.=52'


def test_marktools_TempoMark___init___02():
    r'''Init tempo mark with float-valued mark.
    '''

    tempomark = marktools.TempoMark(Duration(3, 32), 52.5)
    assert format(tempomark) == '\\tempo 16.=52.5'


def test_marktools_TempoMark___init___03():
    r'''Init tempo mark from tempo mark.
    '''

    tempomark = marktools.TempoMark(Duration(3, 32), 52)
    new = marktools.TempoMark(tempomark)

    assert tempomark == new
    assert tempomark is not new

    assert tempomark.duration == new.duration
    assert tempomark.duration is not new.duration


def test_marktools_TempoMark___init___04():
    r'''Init tempo mark from integer pair.
    '''

    tempomark = marktools.TempoMark((3, 32), 52.5)
    assert format(tempomark) == '\\tempo 16.=52.5'


def test_marktools_TempoMark___init___05():
    r'''Init tempo mark from textual indication.
    '''

    tempomark = marktools.TempoMark('Langsam')
    assert format(tempomark) == '\\tempo Langsam'


def test_marktools_TempoMark___init___06():
    r'''Init tempo mark with tempo range.
    '''

    tempomark = marktools.TempoMark((1, 8), (52, 57.5))
    assert format(tempomark) == '\\tempo 8=52-57.5'


def test_marktools_TempoMark___init___07():
    r'''Init tempo mark from text, duration and range.
    '''

    tempomark = marktools.TempoMark('Quick', Duration(1, 4), (120, 133))
    assert format(tempomark) == '\\tempo Quick 4=120-133'


def test_marktools_TempoMark___init___08():
    r'''Init tempo mark from length-2 tuple.
    '''

    tempomark = marktools.TempoMark((Duration(1, 4), (120, 133)))
    assert format(tempomark) == '\\tempo 4=120-133'


def test_marktools_TempoMark___init___09():
    r'''Init tempo mark from length-3 tuple.
    '''

    tempomark = marktools.TempoMark(('Quick', Duration(1, 4), (120, 133)))
    assert format(tempomark) == '\\tempo Quick 4=120-133'
