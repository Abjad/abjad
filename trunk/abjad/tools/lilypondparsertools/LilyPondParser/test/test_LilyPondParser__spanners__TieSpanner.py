import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__TieSpanner_01():
    target = Container([Note(0, 1), Note(0, 1)])
    tietools.TieSpanner(target[:])
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__TieSpanner_02():
    input = r'{ c ~ }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__TieSpanner_03():
    input = r'{ ~ c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__TieSpanner_04():
    '''With direction.'''
    target = Container([Note(0, 1), Note(0, 1)])
    tietools.TieSpanner(target[:], direction='up')
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__TieSpanner_05():
    '''With direction.'''
    target = Container([Note(0, 1), Note(0, 1)])
    tietools.TieSpanner(target[:], direction='down')
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
