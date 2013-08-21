# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__Articulation_01():
    target = Staff(notetools.make_notes(["c''"], [(1, 4)] * 6 + [(1, 2)]))
    marktools.Articulation('marcato', Up)(target[0])
    marktools.Articulation('stopped', Down)(target[1])
    marktools.Articulation('tenuto')(target[2])
    marktools.Articulation('staccatissimo')(target[3])
    marktools.Articulation('accent')(target[4])
    marktools.Articulation('staccato')(target[5])
    marktools.Articulation('portato')(target[6])

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

    input = r'''\new Staff { c''4^^ c''_+ c''-- c''-| c''4-> c''-. c''2-_ }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result
    for x in result:
        assert 1 == len(inspect(x).get_marks(marktools.Articulation))


def test_LilyPondParser__marks__Articulation_02():
    target = Staff([Note("c'", (1, 4))])
    marktools.Articulation('marcato', Up)(target[0])
    marktools.Articulation('stopped', Down)(target[0])
    marktools.Articulation('tenuto')(target[0])
    marktools.Articulation('staccatissimo')(target[0])
    marktools.Articulation('accent')(target[0])
    marktools.Articulation('staccato')(target[0])
    marktools.Articulation('portato')(target[0])

    r'''
    \new Staff {
        c'4 ^\marcato _\stopped -\tenuto -\staccatissimo -\accent -\staccato -\portato
    }
    '''

    input = r'''\new Staff { c'4 ^^ _+ -- -| -> -. -_ }'''


    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 7 == len(inspect(result[0]).get_marks(marktools.Articulation))


def test_LilyPondParser__marks__Articulation_03():
    target = Container(notetools.make_notes(
        ["c''", "c''", "b'", "c''"],
        [(1, 4), (1, 4), (1, 2), (1, 1)]))
    marktools.Articulation('staccato')(target[0])
    marktools.Articulation('mordent')(target[1])
    marktools.Articulation('turn')(target[2])
    marktools.Articulation('fermata')(target[3])

    r'''
    {
        c''4 -\staccato
        c''4 -\mordent
        b'2 -\turn
        c''1 -\fermata
    }
    '''

    input = r'''{ c''4\staccato c''\mordent b'2\turn c''1\fermata }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result
    for x in result:
        assert 1 == len(inspect(x).get_marks(marktools.Articulation))
