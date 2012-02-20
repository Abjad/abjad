import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__BeamSpanner_01():
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.BeamSpanner(target[0:3])
    spannertools.BeamSpanner(target[3:])

    r'''{
        c'4 [
        c'4 
        c'4 ]
        c'4 [ ]
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__BeamSpanner_02():
    '''With start and stop reversed.'''
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.BeamSpanner(target[0:3])
    spannertools.BeamSpanner(target[3:])

    r'''{
        c'4 [
        c'4 
        c'4 ]
        c'4 [ ]
    }
    '''

    input = r'''\relative c' { c [ c c ] c ] [ }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__BeamSpanner_03():
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.BeamSpanner(target[:])
    spannertools.BeamSpanner(target[1:3])

    r'''{
        c'4 [
        c'4 [
        c'4 ]
        c'4 ]
    }
    '''

    assert py.test.raises(Exception, "LilyPondParser()(target.format)")


def test_LilyPondParser__spanners__BeamSpanner_04():
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.BeamSpanner(target[:3])
    spannertools.BeamSpanner(target[2:])

    r'''{
        c'4 [
        c'4 
        c'4 ] [
        c'4 ]
    }
    '''

    assert py.test.raises(Exception, "LilyPondParser()(target.format)")


def test_LilyPondParser__spanners__BeamSpanner_05():
    input = "{ c'4 [ c'4 c'4 c'4 }"
    assert py.test.raises(Exception, "LilyPondParser()(input)")


def test_LilyPondParser__spanners__BeamSpanner_06():
    input = "{ c'4 c'4 c'4 c'4 ] }"
    result = LilyPondParser()(input)
    assert not result[-1].spanners


def test_LilyPondParser__spanners__BeamSpanner_07():
    '''With direction.'''
    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    spannertools.BeamSpanner(target[0:3], direction='up')
    spannertools.BeamSpanner(target[3:], direction='down')

    r'''{
        c'4 ^ [
        c'4 
        c'4 ]
        c'4 _ [ ]
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
