import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__TextSpanner_01():
    '''Successful text spanners, showing single leaf overlap.'''
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.TextSpanner(target[2:])
    spannertools.TextSpanner(target[:3])

    r'''{
        c'4 \startTextSpan
        c'4
        c'4 \stopTextSpan \startTextSpan
        c'4 \stopTextSpan
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__TextSpanner_02():
    '''Swapped start and stop.'''
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.TextSpanner(target[2:])
    spannertools.TextSpanner(target[:3])

    r'''{
        c'4 \startTextSpan
        c'4
        c'4 \stopTextSpan \startTextSpan
        c'4 \stopTextSpan
    }
    '''

    input = r"\relative c' { c \startTextSpan c c \startTextSpan \stopTextSpan c \stopTextSpan }"

    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__TextSpanner_03():
    '''Single leaf.'''
    input = r'{ c \startTextSpan \stopTextSpan c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__TextSpanner_04():
    '''Unterminated.'''
    input = r'{ c \startTextSpan c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__TextSpanner_05():
    '''Unstarted.'''
    input = r'{ c c c c \stopTextSpan }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__TextSpanner_06():
    '''Nested.'''
    input = r'{ c \startTextSpan c \startTextSpan c \stopTextSpan c \stopTextSpan }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')
