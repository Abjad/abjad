import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__HorizontalBracketSpanner_01():
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.HorizontalBracketSpanner(target[:])
    spannertools.HorizontalBracketSpanner(target[:2])
    spannertools.HorizontalBracketSpanner(target[2:])

    r'''{
        c'4 \startGroup \startGroup
        c'4 \stopGroup
        c'4 \startGroup
        c'4 \stopGroup \stopGroup
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__HorizontalBracketSpanner_02():
    '''Starting and stopping on the same leaf.'''
    input = r'''{ c \startGroup \stopGroup c c c }'''
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__HorizontalBracketSpanner_03():
    '''One group stopping on a leaf, while another begins on the same leaf.'''
    input = r'''{ c \startGroup c \stopGroup \startGroup c c \stopGroup }'''
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__HorizontalBracketSpanner_04():
    '''Unterminated.'''
    input = r'''{ c \startGroup c c c }'''
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__HorizontalBracketSpanner_05():
    '''Unstarted.'''
    input = r'''{ c c c c \stopGroup }'''
    assert py.test.raises(Exception, 'LilyPondParser()(input)')
