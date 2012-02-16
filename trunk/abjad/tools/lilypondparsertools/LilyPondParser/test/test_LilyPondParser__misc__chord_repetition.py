import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__misc__chord_repetition_01():
    target = Container([
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (1, 4)),
    ])

    r'''{
        <c' e' g'>4
        <c' e' g'>4
        <c' e' g'>4
        <c' e' g'>4
    }
    '''

    input = r'''{ <c' e' g'> q q q }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__misc__chord_repetition_02():
    target = Staff([
        Chord([0, 4, 7], (1, 8)),
        Chord([0, 4, 7], (1, 8)),
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (3, 16)),
        Chord([0, 4, 7], (1, 16)),
        Chord([0, 4, 7], (1, 4))
    ])
    contexttools.DynamicMark('p')(target[0])
    marktools.Articulation('staccatissimo')(target[2])
    markuptools.Markup('text', 'up')(target[3])
    marktools.Articulation('staccatissimo')(target[-1])

    r'''\new Staff {
        <c' e' g'>8 \p
        <c' e' g'>8
        <c' e' g'>4 -\staccatissimo
        <c' e' g'>8. ^ \markup { text }
        <c' e' g'>16
        <c' e' g'>4 -\staccatissimo
    }
    '''

    input = r'''\new Staff { <c' e' g'>8\p q q4-| q8.^"text" q16 q4-| }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__misc__chord_repetition_03():
    target = Container([
        Chord([0, 4, 7], (1, 8)),
        Note(12, (1, 8)),
        Chord([0, 4, 7], (1, 8)),
        Note(12, (1, 8)),
        Rest((1, 4)),
        Chord([0, 4, 7], (1, 4)),
    ])

    r'''{
        <c' e' g'>8
        c''8
        <c' e' g'>8
        c''8
        r4
        <c' e' g'>4
    }
    '''

    input = r'''{ <c' e' g'>8 c'' q c'' r4 q }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result
