# -*- encoding: utf-8 -*-
from abjad import *


def test_TempoMark___init___01():
    r'''Init tempo mark with integer-valued mark.
    '''

    tempomark = contexttools.TempoMark(Duration(3, 32), 52)
    assert tempomark.lilypond_format == '\\tempo 16.=52'


def test_TempoMark___init___02():
    r'''Init tempo mark with float-valued mark.
    '''

    tempomark = contexttools.TempoMark(Duration(3, 32), 52.5)
    assert tempomark.lilypond_format == '\\tempo 16.=52.5'


def test_TempoMark___init___03():
    r'''Init tempo mark from tempo mark.
    '''

    tempomark = contexttools.TempoMark(Duration(3, 32), 52)
    new = contexttools.TempoMark(tempomark)

    assert tempomark == new
    assert tempomark is not new

    assert tempomark.duration == new.duration
    assert tempomark.duration is not new.duration


def test_TempoMark___init___04():
    r'''Init tempo mark from integer pair.
    '''

    tempomark = contexttools.TempoMark((3, 32), 52.5)
    assert tempomark.lilypond_format == '\\tempo 16.=52.5'


def test_TempoMark___init___05():
    r'''Init tempo mark from textual indication.
    '''

    tempomark = contexttools.TempoMark('Langsam')
    assert tempomark.lilypond_format == '\\tempo Langsam'


def test_TempoMark___init___06():
    r'''Init tempo mark with tempo range.
    '''

    tempomark = contexttools.TempoMark((1, 8), (52, 57.5))
    assert tempomark.lilypond_format == '\\tempo 8=52-57.5'


def test_TempoMark___init___07():
    r'''Init tempo mark from text, duration and range.
    '''

    tempomark = contexttools.TempoMark('Quick', Duration(1, 4), (120, 133))
    assert tempomark.lilypond_format == '\\tempo Quick 4=120-133'


def test_TempoMark___init___08():
    r'''Init tempo mark from length-2 tuple.
    '''

    tempomark = contexttools.TempoMark((Duration(1, 4), (120, 133)))
    assert tempomark.lilypond_format == '\\tempo 4=120-133'


def test_TempoMark___init___09():
    r'''Init tempo mark from length-3 tuple.
    '''

    tempomark = contexttools.TempoMark(('Quick', Duration(1, 4), (120, 133)))
    assert tempomark.lilypond_format == '\\tempo Quick 4=120-133'
