# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo___init___01():
    r'''Initialize tempo with integer.
    '''

    tempo = Tempo(Duration(3, 32), 52)
    assert format(tempo, 'lilypond') == '\\tempo 16.=52'


def test_indicatortools_Tempo___init___02():
    r'''Initialize tempo with float.
    '''

    tempo = Tempo(Duration(3, 32), 52.5)
    assert format(tempo, 'lilypond') == '\\tempo 16.=52.5'


def test_indicatortools_Tempo___init___03():
    r'''Initialize tempo from tempo.
    '''

    tempo = Tempo(Duration(3, 32), 52)
    new = Tempo(tempo)

    assert tempo == new
    assert tempo is not new

    assert tempo.duration == new.duration
    assert tempo.duration is not new.duration


def test_indicatortools_Tempo___init___04():
    r'''Initialize tempo from integer pair.
    '''

    tempo = Tempo((3, 32), 52.5)
    assert format(tempo, 'lilypond') == '\\tempo 16.=52.5'


def test_indicatortools_Tempo___init___05():
    r'''Initialize tempo from textual indication.
    '''

    tempo = Tempo('Langsam')
    assert format(tempo, 'lilypond') == '\\tempo Langsam'


def test_indicatortools_Tempo___init___06():
    r'''Initialize tempo with tempo range.
    '''

    tempo = Tempo((1, 8), (52, 57.5))
    assert format(tempo, 'lilypond') == '\\tempo 8=52-57.5'


def test_indicatortools_Tempo___init___07():
    r'''Initialize tempo from text, duration and range.
    '''

    tempo = Tempo('Quick', Duration(1, 4), (120, 133))
    assert format(tempo, 'lilypond') == '\\tempo Quick 4=120-133'


def test_indicatortools_Tempo___init___08():
    r'''Initialize tempo from length-2 tuple.
    '''

    tempo = Tempo((Duration(1, 4), (120, 133)))
    assert format(tempo, 'lilypond') == '\\tempo 4=120-133'


def test_indicatortools_Tempo___init___09():
    r'''Initialize tempo from length-3 tuple.
    '''

    tempo = Tempo(('Quick', Duration(1, 4), (120, 133)))
    assert format(tempo, 'lilypond') == '\\tempo Quick 4=120-133'
