# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_01():

    target = Container([Note(0, 1), Note(0, 1)])
    tie = spannertools.Tie()
    attach(tie, target[:])
    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_02():

    string = r'{ c ~ }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_03():

    string = r'{ ~ c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_04():
    r'''With direction.
    '''

    target = Container([Note(0, 1), Note(0, 1)])
    tie = spannertools.Tie(direction=Up)
    attach(tie, target[:])
    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_05():
    r'''With direction.
    '''

    target = Container([Note(0, 1), Note(0, 1)])
    tie = spannertools.Tie(direction=Down)
    attach(tie, target[:])
    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
