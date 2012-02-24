import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__HairpinSpanner_01():
    target = Staff(notetools.make_notes([0] * 5, [(1, 4)]))
    spannertools.HairpinSpanner(target[:3], '<')
    spannertools.HairpinSpanner(target[2:], '>')
    contexttools.DynamicMark('ppp')(target[-1])

    r'''\new Staff {
        c'4 \<
        c'4
        c'4 \! \>
        c'4
        c'4 \ppp
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__HairpinSpanner_02():
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.HairpinSpanner(target[0:2], '<')
    spannertools.HairpinSpanner(target[1:3], '<')
    spannertools.HairpinSpanner(target[2:], '<')

    r'''{
        c'4 \<
        c'4 \! \<
        c'4 \! \<
        c'4 \!
    }
    '''

    input = r'''\relative c' { c \< c \< c \< c \! }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__HairpinSpanner_03():
    '''Dynamic marks can terminate hairpins.'''
    target = Staff(notetools.make_notes([0] * 3, [(1, 4)]))
    spannertools.HairpinSpanner(target[0:2], '<')
    spannertools.HairpinSpanner(target[1:], '>')
    contexttools.DynamicMark('p')(target[1])
    contexttools.DynamicMark('f')(target[-1])

    r'''\new Staff {
        c'4 \<
        c'4 \p \>
        c'4 \f
    }
    '''

    input = r"\new Staff \relative c' { c \< c \p \> c \f }"
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__HairpinSpanner_04():
    '''Unterminated.'''
    input = r'{ c \< c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__HairpinSpanner_05():
    '''Unbegun is okay.'''
    input = r'{ c c c c \! }'
    result = LilyPondParser()(input)


def test_LilyPondParser__spanners__HairpinSpanner_06():
    '''No double dynamic spans permitted.'''
    input = r'{ c \< \> c c c \! }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__HairpinSpanner_07():
    '''With direction.'''
    target = Staff(notetools.make_notes([0] * 5, [(1, 4)]))
    spannertools.HairpinSpanner(target[:3], '<', direction = 'up')
    spannertools.HairpinSpanner(target[2:], '>', direction = 'down')
    contexttools.DynamicMark('ppp')(target[-1])

    r'''\new Staff {
        c'4 ^ \<
        c'4
        c'4 \! _ \>
        c'4
        c'4 \ppp
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
