# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__misc__chord_repetition_01():

    target = Container([
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (1, 4)),
    ])

    assert format(target) == stringtools.normalize(
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
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__misc__chord_repetition_02():

    target = Staff([
        Chord([0, 4, 7], (1, 8)),
        Chord([0, 4, 7], (1, 8)),
        Chord([0, 4, 7], (1, 4)),
        Chord([0, 4, 7], (3, 16)),
        Chord([0, 4, 7], (1, 16)),
        Chord([0, 4, 7], (1, 4))
    ])

    dynamic = Dynamic('p')
    attach(dynamic, target[0])
    articulation = Articulation('staccatissimo')
    attach(articulation, target[2])
    markup = markuptools.Markup('text', Up)
    attach(markup, target[3])
    articulation = Articulation('staccatissimo')
    attach(articulation, target[-1])

    assert format(target) == stringtools.normalize(
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
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__misc__chord_repetition_03():

    target = Container([
        Chord([0, 4, 7], (1, 8)),
        Note(12, (1, 8)),
        Chord([0, 4, 7], (1, 8)),
        Note(12, (1, 8)),
        Rest((1, 4)),
        Chord([0, 4, 7], (1, 4)),
    ])

    assert format(target) == stringtools.normalize(
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
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
