import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__misc__chord_repetition_01():

    target = abjad.Container([
        abjad.Chord([0, 4, 7], (1, 4)),
        abjad.Chord([0, 4, 7], (1, 4)),
        abjad.Chord([0, 4, 7], (1, 4)),
        abjad.Chord([0, 4, 7], (1, 4)),
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            <c' e' g'>4
            <c' e' g'>4
            <c' e' g'>4
            <c' e' g'>4
        }
        '''
        )

    string = r'''{ <c' e' g'> q q q }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__misc__chord_repetition_02():

    target = abjad.Staff([
        abjad.Chord([0, 4, 7], (1, 8)),
        abjad.Chord([0, 4, 7], (1, 8)),
        abjad.Chord([0, 4, 7], (1, 4)),
        abjad.Chord([0, 4, 7], (3, 16)),
        abjad.Chord([0, 4, 7], (1, 16)),
        abjad.Chord([0, 4, 7], (1, 4))
    ])

    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, target[0])
    articulation = abjad.Articulation('staccatissimo')
    abjad.attach(articulation, target[2])
    markup = abjad.Markup('text', abjad.Up)
    abjad.attach(markup, target[3])
    articulation = abjad.Articulation('staccatissimo')
    abjad.attach(articulation, target[-1])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            <c' e' g'>8 \p
            <c' e' g'>8
            <c' e' g'>4 -\staccatissimo
            <c' e' g'>8. ^ \markup { text }
            <c' e' g'>16
            <c' e' g'>4 -\staccatissimo
        }
        '''
        )

    string = r'''\new Staff { <c' e' g'>8\p q q4-| q8.^"text" q16 q4-| }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__misc__chord_repetition_03():

    target = abjad.Container([
        abjad.Chord([0, 4, 7], (1, 8)),
        abjad.Note(12, (1, 8)),
        abjad.Chord([0, 4, 7], (1, 8)),
        abjad.Note(12, (1, 8)),
        abjad.Rest((1, 4)),
        abjad.Chord([0, 4, 7], (1, 4)),
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            <c' e' g'>8
            c''8
            <c' e' g'>8
            c''8
            r4
            <c' e' g'>4
        }
        '''
        )

    string = r'''{ <c' e' g'>8 c'' q c'' r4 q }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
