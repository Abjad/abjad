# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__Beam_01():

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    beam = Beam()
    attach(beam, target[0:3])
    beam = Beam()
    attach(beam, target[3:])

    assert format(target) == stringtools.normalize(
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Beam_02():
    r'''With start and stop reversed.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    beam = Beam()
    attach(beam, target[0:3])
    beam = Beam()
    attach(beam, target[3:])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4 [
            c'4
            c'4 ]
            c'4 [ ]
        }
        '''
        )

    string = r'''\relative c' { c [ c c ] c ] [ }'''
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Beam_03():

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    beam = Beam()
    attach(beam, target[:])
    beam = Beam()
    attach(beam, target[1:3])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4 [
            c'4 [
            c'4 ]
            c'4 ]
        }
        '''
        )

    assert pytest.raises(Exception, "LilyPondParser()(format(target))")


def test_lilypondparsertools_LilyPondParser__spanners__Beam_04():

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    beam = Beam()
    attach(beam, target[:3])
    beam = Beam()
    attach(beam, target[2:])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4 [
            c'4
            c'4 ] [
            c'4 ]
        }
        '''
        )

    assert pytest.raises(Exception, "LilyPondParser()(format(target))")


def test_lilypondparsertools_LilyPondParser__spanners__Beam_05():

    string = "{ c'4 [ c'4 c'4 c'4 }"
    assert pytest.raises(Exception, "LilyPondParser()(string)")


def test_lilypondparsertools_LilyPondParser__spanners__Beam_06():

    string = "{ c'4 c'4 c'4 c'4 ] }"
    result = LilyPondParser()(string)
    assert not inspect_(result[-1]).get_spanners()


def test_lilypondparsertools_LilyPondParser__spanners__Beam_07():
    r'''With direction.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    beam = Beam(direction=Up)
    attach(beam, target[0:3])
    beam = Beam(direction=Down)
    attach(beam, target[3:])

    assert format(target) == stringtools.normalize(
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
