# -*- coding: utf-8 -*-
import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__Tie_01():

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    tie = abjad.Tie()
    abjad.attach(tie, target[:])
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Tie_02():

    string = r'{ c ~ }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Tie_03():

    string = r'{ ~ c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Tie_04():
    r'''With direction.
    '''

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    tie = abjad.Tie(direction=Up)
    abjad.attach(tie, target[:])
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Tie_05():
    r'''With direction.
    '''

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    tie = abjad.Tie(direction=Down)
    abjad.attach(tie, target[:])
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
