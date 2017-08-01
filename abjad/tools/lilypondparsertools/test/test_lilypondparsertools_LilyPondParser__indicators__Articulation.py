# -*- coding: utf-8 -*-
import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__indicators__Articulation_01():

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker(["c''"], [(1, 4)] * 6 + [(1, 2)]))
    articulation = abjad.Articulation('marcato', Up)
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('stopped', Down)
    abjad.attach(articulation, target[1])
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, target[2])
    articulation = abjad.Articulation('staccatissimo')
    abjad.attach(articulation, target[3])
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, target[4])
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, target[5])
    articulation = abjad.Articulation('portato')
    abjad.attach(articulation, target[6])

    assert format(target) == abjad.String.normalize(
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

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and \
        target is not result
    for x in result:
        assert 1 == len(abjad.inspect(x).get_indicators(abjad.Articulation))


def test_lilypondparsertools_LilyPondParser__indicators__Articulation_02():

    target = abjad.Staff([abjad.Note("c'", (1, 4))])
    articulation = abjad.Articulation('marcato', Up)
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('stopped', Down)
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('staccatissimo')
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('portato')
    abjad.attach(articulation, target[0])

    r'''
    \new Staff {
        c'4 ^\marcato _\stopped -\tenuto -\staccatissimo -\accent -\staccato -\portato
    }
    '''

    string = r'''\new Staff { c'4 ^^ _+ -- -| -> -. -_ }'''


    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and \
        target is not result
    assert 7 == len(abjad.inspect(result[0]).get_indicators(abjad.Articulation))


def test_lilypondparsertools_LilyPondParser__indicators__Articulation_03():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker(
        ["c''", "c''", "b'", "c''"],
        [(1, 4), (1, 4), (1, 2), (1, 1)]
        ))

    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation('mordent')
    abjad.attach(articulation, target[1])
    articulation = abjad.Articulation('turn')
    abjad.attach(articulation, target[2])
    articulation = abjad.Articulation('fermata')
    abjad.attach(articulation, target[3])

    assert format(target) == abjad.String.normalize(
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

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and \
        target is not result
    for x in result:
        assert 1 == len(abjad.inspect(x).get_indicators(abjad.Articulation))
