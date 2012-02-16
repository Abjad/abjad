import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__PhrasingSlurSpanner_01():
    '''Successful slurs, showing single leaf overlap.'''
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.PhrasingSlurSpanner(target[2:])
    spannertools.PhrasingSlurSpanner(target[:3])

    r'''{
        c'4 \(
        c'4
        c'4 \) \(
        c'4 \)
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__PhrasingSlurSpanner_02():
    '''Swapped start and stop.'''
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.PhrasingSlurSpanner(target[2:])
    spannertools.PhrasingSlurSpanner(target[:3])

    r'''{
        c'4 \(
        c'4
        c'4 \) \(
        c'4 \)
    }
    '''

    input = r"\relative c' { c \( c c \( \) c \) }"

    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__PhrasingSlurSpanner_03():
    '''Single leaf.'''
    input = '{ c \( \) c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__PhrasingSlurSpanner_04():
    '''Unterminated.'''
    input = '{ c \( c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__PhrasingSlurSpanner_05():
    '''Unstarted.'''
    input = '{ c c c c \) }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__PhrasingSlurSpanner_06():
    '''Nested.'''
    input = '{ c \( c \( c \) c \) }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')
