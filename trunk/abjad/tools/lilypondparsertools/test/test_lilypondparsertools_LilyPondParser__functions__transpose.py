# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__functions__transpose_01():

    pitches = ["e'", "gs'", "b'", "e''"]
    target = Staff(notetools.make_notes(pitches, (1, 4)))
    key_signature = contexttools.KeySignatureMark('e', 'major')
    attach(key_signature, target[0])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            \key e \major
            e'4
            gs'4
            b'4
            e''4
        }
        '''
        )

    string = r"\transpose d e \relative c' \new Staff { \key d \major d4 fs a d }"
    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__functions__transpose_02():

    pitches = ["ef'", "f'", "g'", "bf'"]
    target = Staff(notetools.make_notes(pitches, (1, 4)))
    key_signature = contexttools.KeySignatureMark('ef', 'major')
    attach(key_signature, target[0])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            \key ef \major
            ef'4
            f'4
            g'4
            bf'4
        }
        '''
        )

    string = r"\transpose a c' \relative c' \new Staff { \key c \major c4 d e g }"
    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__functions__transpose_03():

    target = Staff([
        Container(notetools.make_notes(["cs'", "ds'", "es'", "fs'"], (1, 4))),
        Container(notetools.make_notes(["df'", "ef'", "f'", "gf'"], (1, 4)))
    ])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            {
                cs'4
                ds'4
                es'4
                fs'4
            }
            {
                df'4
                ef'4
                f'4
                gf'4
            }
        }
        '''
        )

    string = r'''music = \relative c' { c d e f }
    \new Staff {
        \transpose c cs \music
        \transpose c df \music
    }
    '''

    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and target is not result
