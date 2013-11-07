# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoMark___init___01():
    r'''Init tempo mark with integer-valued mark.
    '''

    tempo_mark = marktools.TempoMark(Duration(3, 32), 52)
    assert format(tempo_mark, 'lilypond') == '\\tempo 16.=52'


def test_marktools_TempoMark___init___02():
    r'''Init tempo mark with float-valued mark.
    '''

    tempo_mark = marktools.TempoMark(Duration(3, 32), 52.5)
    assert format(tempo_mark, 'lilypond') == '\\tempo 16.=52.5'


def test_marktools_TempoMark___init___03():
    r'''Init tempo mark from tempo mark.
    '''

    tempo_mark = marktools.TempoMark(Duration(3, 32), 52)
    new = marktools.TempoMark(tempo_mark)

    assert tempo_mark == new
    assert tempo_mark is not new

    assert tempo_mark.duration == new.duration
    assert tempo_mark.duration is not new.duration


def test_marktools_TempoMark___init___04():
    r'''Init tempo mark from integer pair.
    '''

    tempo_mark = marktools.TempoMark((3, 32), 52.5)
    assert format(tempo_mark, 'lilypond') == '\\tempo 16.=52.5'


def test_marktools_TempoMark___init___05():
    r'''Init tempo mark from textual indication.
    '''

    tempo_mark = marktools.TempoMark('Langsam')
    assert format(tempo_mark, 'lilypond') == '\\tempo Langsam'


def test_marktools_TempoMark___init___06():
    r'''Init tempo mark with tempo range.
    '''

    tempo_mark = marktools.TempoMark((1, 8), (52, 57.5))
    assert format(tempo_mark, 'lilypond') == '\\tempo 8=52-57.5'


def test_marktools_TempoMark___init___07():
    r'''Init tempo mark from text, duration and range.
    '''

    tempo_mark = marktools.TempoMark('Quick', Duration(1, 4), (120, 133))
    assert format(tempo_mark, 'lilypond') == '\\tempo Quick 4=120-133'


def test_marktools_TempoMark___init___08():
    r'''Init tempo mark from length-2 tuple.
    '''

    tempo_mark = marktools.TempoMark((Duration(1, 4), (120, 133)))
    assert format(tempo_mark, 'lilypond') == '\\tempo 4=120-133'


def test_marktools_TempoMark___init___09():
    r'''Init tempo mark from length-3 tuple.
    '''

    tempo_mark = marktools.TempoMark(('Quick', Duration(1, 4), (120, 133)))
    assert format(tempo_mark, 'lilypond') == '\\tempo Quick 4=120-133'
