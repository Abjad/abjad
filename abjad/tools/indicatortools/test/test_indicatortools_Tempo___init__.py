# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo___init___01():
    r'''Initializes tempo with integer.
    '''

    tempo = Tempo(Duration(3, 32), 52)
    assert format(tempo, 'lilypond') == '\\tempo 16.=52'


def test_indicatortools_Tempo___init___02():
    r'''Initializes tempo from textual indication.
    '''

    tempo = Tempo(textual_indication='Langsam')
    assert format(tempo, 'lilypond') == '\\tempo Langsam'


def test_indicatortools_Tempo___init___03():
    r'''Initializes tempo with tempo range.
    '''

    tempo = Tempo((1, 8), (52, 57.5))
    assert format(tempo, 'lilypond') == '\\tempo 8=52-57.5'


def test_indicatortools_Tempo___init___04():
    r'''Initializes tempo from text, duration and range.
    '''

    tempo = Tempo(Duration(1, 4), (120, 133), 'Quick')
    assert format(tempo, 'lilypond') == '\\tempo Quick 4=120-133'
