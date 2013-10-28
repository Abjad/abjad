# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_01():

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    beam = spannertools.BeamSpanner()
    attach(beam, target[0:3])
    beam = spannertools.BeamSpanner()
    attach(beam, target[3:])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 [
            c'4
            c'4 ]
            c'4 [ ]
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_02():
    r'''With start and stop reversed.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    beam = spannertools.BeamSpanner()
    attach(beam, target[0:3])
    beam = spannertools.BeamSpanner()
    attach(beam, target[3:])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 [
            c'4
            c'4 ]
            c'4 [ ]
        }
        '''
        )

    input = r'''\relative c' { c [ c c ] c ] [ }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_03():

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    beam = spannertools.BeamSpanner()
    attach(beam, target[:])
    beam = spannertools.BeamSpanner()
    attach(beam, target[1:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 [
            c'4 [
            c'4 ]
            c'4 ]
        }
        '''
        )

    assert py.test.raises(Exception, "LilyPondParser()(target.lilypond_format)")


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_04():

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    beam = spannertools.BeamSpanner()
    attach(beam, target[:3])
    beam = spannertools.BeamSpanner()
    attach(beam, target[2:])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 [
            c'4
            c'4 ] [
            c'4 ]
        }
        '''
        )

    assert py.test.raises(Exception, "LilyPondParser()(target.lilypond_format)")


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_05():

    string = "{ c'4 [ c'4 c'4 c'4 }"
    assert py.test.raises(Exception, "LilyPondParser()(string)")


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_06():

    string = "{ c'4 c'4 c'4 c'4 ] }"
    result = LilyPondParser()(string)
    assert not inspect(result[-1]).get_spanners()


def test_lilypondparsertools_LilyPondParser__spanners__BeamSpanner_07():
    r'''With direction.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    beam = spannertools.BeamSpanner(direction=Up)
    attach(beam, target[0:3])
    beam = spannertools.BeamSpanner(direction=Down)
    attach(beam, target[3:])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 ^ [
            c'4
            c'4 ]
            c'4 _ [ ]
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
