# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_01():

    target = Score([Staff([Note(0, 1)])])
    tempo = Tempo("As fast as possible", _target_context=Staff)
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
    result = parser(format(target))
    assert format(target) == format(result) and \
        target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(Tempo)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_02():

    target = Score([Staff([Note(0, 1)])])
    tempo = Tempo((1, 4), 60, _target_context=Staff)
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(Tempo)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_03():

    target = Score([Staff([Note(0, 1)])])
    tempo = Tempo((1, 4), (59, 63), _target_context=Staff)
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(Tempo)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_04():

    target = Score([Staff([Note(0, 1)])])
    tempo = Tempo(
        "Like a majestic swan, alive with youth and vigour!",
        (1, 4), 
        60, 
        _target_context=Staff,
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(Tempo)
    assert len(tempo_marks) == 1


def test_lilypondparsertools_LilyPondParser__marks__TempoMark_05():

    target = Score([Staff([Note(0, 1)])])
    tempo = Tempo(
        "Faster than a thousand suns",
        (1, 16), (34, 55), 
        _target_context=Staff,
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaf = result.select_leaves()[0]
    tempo_marks = inspect(leaf).get_marks(Tempo)
    assert len(tempo_marks) == 1
