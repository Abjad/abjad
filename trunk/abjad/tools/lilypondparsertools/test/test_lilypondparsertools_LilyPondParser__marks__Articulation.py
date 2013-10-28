# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__Articulation_01():

    target = Staff(notetools.make_notes(["c''"], [(1, 4)] * 6 + [(1, 2)]))
    articulation = marktools.Articulation('marcato', Up)
    attach(articulation, target[0])
    articulation = marktools.Articulation('stopped', Down)
    attach(articulation, target[1])
    articulation = marktools.Articulation('tenuto')
    attach(articulation, target[2])
    articulation = marktools.Articulation('staccatissimo')
    attach(articulation, target[3])
    articulation = marktools.Articulation('accent')
    attach(articulation, target[4])
    articulation = marktools.Articulation('staccato')
    attach(articulation, target[5])
    articulation = marktools.Articulation('portato')
    attach(articulation, target[6])

    assert testtools.compare(
        target,
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
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    for x in result:
        assert 1 == len(inspect(x).get_marks(marktools.Articulation))


def test_lilypondparsertools_LilyPondParser__marks__Articulation_02():

    target = Staff([Note("c'", (1, 4))])
    articulation = marktools.Articulation('marcato', Up)
    attach(articulation, target[0])
    articulation = marktools.Articulation('stopped', Down)
    attach(articulation, target[0])
    articulation = marktools.Articulation('tenuto')
    attach(articulation, target[0])
    articulation = marktools.Articulation('staccatissimo')
    attach(articulation, target[0])
    articulation = marktools.Articulation('accent')
    attach(articulation, target[0])
    articulation = marktools.Articulation('staccato')
    attach(articulation, target[0])
    articulation = marktools.Articulation('portato')
    attach(articulation, target[0])

    r'''
    \new Staff {
        c'4 ^\marcato _\stopped -\tenuto -\staccatissimo -\accent -\staccato -\portato
    }
    '''

    string = r'''\new Staff { c'4 ^^ _+ -- -| -> -. -_ }'''


    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    assert 7 == len(inspect(result[0]).get_marks(marktools.Articulation))


def test_lilypondparsertools_LilyPondParser__marks__Articulation_03():

    target = Container(notetools.make_notes(
        ["c''", "c''", "b'", "c''"],
        [(1, 4), (1, 4), (1, 2), (1, 1)]))

    articulation = marktools.Articulation('staccato')
    attach(articulation, target[0])
    articulation = marktools.Articulation('mordent')
    attach(articulation, target[1])
    articulation = marktools.Articulation('turn')
    attach(articulation, target[2])
    articulation = marktools.Articulation('fermata')
    attach(articulation, target[3])

    assert testtools.compare(
        target,
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
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    for x in result:
        assert 1 == len(inspect(x).get_marks(marktools.Articulation))
