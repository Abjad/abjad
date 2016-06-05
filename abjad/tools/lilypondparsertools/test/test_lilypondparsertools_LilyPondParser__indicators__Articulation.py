# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__Articulation_01():

    target = Staff(scoretools.make_notes(["c''"], [(1, 4)] * 6 + [(1, 2)]))
    articulation = Articulation('marcato', Up)
    attach(articulation, target[0])
    articulation = Articulation('stopped', Down)
    attach(articulation, target[1])
    articulation = Articulation('tenuto')
    attach(articulation, target[2])
    articulation = Articulation('staccatissimo')
    attach(articulation, target[3])
    articulation = Articulation('accent')
    attach(articulation, target[4])
    articulation = Articulation('staccato')
    attach(articulation, target[5])
    articulation = Articulation('portato')
    attach(articulation, target[6])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            c''4 ^\marcato
            c''4 _\stopped
            c''4 -\tenuto
            c''4 -\staccatissimo
            c''4 -\accent
            c''4 -\staccato
            c''2 -\portato
        }
        '''
        )

    string = r'''\new Staff { c''4^^ c''_+ c''-- c''-| c''4-> c''-. c''2-_ }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and \
        target is not result
    for x in result:
        assert 1 == len(inspect_(x).get_indicators(Articulation))


def test_lilypondparsertools_LilyPondParser__indicators__Articulation_02():

    target = Staff([Note("c'", (1, 4))])
    articulation = Articulation('marcato', Up)
    attach(articulation, target[0])
    articulation = Articulation('stopped', Down)
    attach(articulation, target[0])
    articulation = Articulation('tenuto')
    attach(articulation, target[0])
    articulation = Articulation('staccatissimo')
    attach(articulation, target[0])
    articulation = Articulation('accent')
    attach(articulation, target[0])
    articulation = Articulation('staccato')
    attach(articulation, target[0])
    articulation = Articulation('portato')
    attach(articulation, target[0])

    r'''
    \new Staff {
        c'4 ^\marcato _\stopped -\tenuto -\staccatissimo -\accent -\staccato -\portato
    }
    '''

    string = r'''\new Staff { c'4 ^^ _+ -- -| -> -. -_ }'''


    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and \
        target is not result
    assert 7 == len(inspect_(result[0]).get_indicators(Articulation))


def test_lilypondparsertools_LilyPondParser__indicators__Articulation_03():

    target = Container(scoretools.make_notes(
        ["c''", "c''", "b'", "c''"],
        [(1, 4), (1, 4), (1, 2), (1, 1)]))

    articulation = Articulation('staccato')
    attach(articulation, target[0])
    articulation = Articulation('mordent')
    attach(articulation, target[1])
    articulation = Articulation('turn')
    attach(articulation, target[2])
    articulation = Articulation('fermata')
    attach(articulation, target[3])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c''4 -\staccato
            c''4 -\mordent
            b'2 -\turn
            c''1 -\fermata
        }
        '''
        )

    string = r'''{ c''4\staccato c''\mordent b'2\turn c''1\fermata }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and \
        target is not result
    for x in result:
        assert 1 == len(inspect_(x).get_indicators(Articulation))
