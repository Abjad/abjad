# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_01():

    target = Score([Staff([Note(0, 1)])])
    tempo = marktools.TempoMark("As fast as possible", target_context=Staff)
    attach(tempo, target.select_leaves()[0])

    assert testtools.compare(
        target,
        r'''
        \new Score <<
            \new Staff {
                \tempo "As fast as possible"
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(marktools.TempoMark)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_02():

    target = Score([Staff([Note(0, 1)])])
    tempo = marktools.TempoMark((1, 4), 60, target_context=Staff)
    attach(tempo, target.select_leaves()[0])

    assert testtools.compare(
        target,
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=60
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(marktools.TempoMark)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_03():

    target = Score([Staff([Note(0, 1)])])
    tempo = marktools.TempoMark((1, 4), (59, 63), target_context=Staff)
    attach(tempo, target.select_leaves()[0])

    assert testtools.compare(
        target,
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=59-63
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(marktools.TempoMark)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_04():

    target = Score([Staff([Note(0, 1)])])
    tempo = marktools.TempoMark(
        "Like a majestic swan, alive with youth and vigour!",
        (1, 4), 
        60, 
        target_context=Staff,
        )
    attach(tempo, target.select_leaves()[0])

    assert testtools.compare(
        target,
        r'''
        \new Score <<
            \new Staff {
                \tempo "Like a majestic swan, alive with youth and vigour!" 4=60
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(marktools.TempoMark)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_05():

    target = Score([Staff([Note(0, 1)])])
    tempo = marktools.TempoMark(
        "Faster than a thousand suns",
        (1, 16), (34, 55), 
        target_context=Staff,
        )
    attach(tempo, target.select_leaves()[0])

    assert testtools.compare(
        target,
        r'''
        \new Score <<
            \new Staff {
                \tempo "Faster than a thousand suns" 16=34-55
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(marktools.TempoMark)
    assert len(tempo_marks) == 1
