# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Container_extend_01():
    r'''Extend container with list of leaves.
    '''

    voice = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice[:])
    voice.extend([Note("c'8"), Note("d'8")])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            c'8
            d'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container_extend_02():
    r'''Extend container with contents of other container.
    '''

    voice_1 = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice_1[:])

    voice_2 = Voice("e'8 f'8")
    beam = Beam()
    attach(beam, voice_2[:])
    voice_1.extend(voice_2)

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
        }
        '''
        )

    assert inspect_(voice_1).is_well_formed()


def test_scoretools_Container_extend_03():
    r'''Extending container with empty list leaves container unchanged.
    '''

    voice = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice[:])
    voice.extend([])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container_extend_04():
    r'''Extending one container with empty second container leaves both
    containers unchanged.
    '''

    voice = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice[:])
    voice.extend(Voice([]))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container_extend_05():
    r'''Trying to extend container with noncomponent raises TypeError.
    '''

    voice = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice[:])

    assert pytest.raises(Exception, 'voice.extend(7)')
    assert pytest.raises(Exception, "voice.extend('foo')")


def test_scoretools_Container_extend_06():
    r'''Trying to extend container with noncontainer raises exception.
    '''

    voice = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice[:])

    statement = 'voice.extend(Note(4, (1, 4)))'
    assert pytest.raises(AttributeError, statement)

    statement = 'voice.extend(Chord([2, 3, 5], (1, 4)))'
    assert pytest.raises(AttributeError, statement)


def test_scoretools_Container_extend_07():
    r'''Extend container with partial and spanned contents of other container.
    '''

    voice_1 = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice_1[:])

    voice_2 = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice_2[:])

    voice_1.extend(voice_2[-2:])

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    assert inspect_(voice_1).is_well_formed()

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert inspect_(voice_2).is_well_formed()


def test_scoretools_Container_extend_08():
    r'''Extend container with partial and spanned contents of other container.
    Covered span comes with components from donor container.
    '''

    voice_1 = Voice("c'8 d'8")
    beam = Beam()
    attach(beam, voice_1[:])

    voice_2 = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice_2[:])
    slur = Slur()
    attach(slur, voice_2[-2:])

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 (
            f'8 ] )
        }
        '''
        )

    voice_1.extend(voice_2[-2:])

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8 (
            f'8 )
        }
        '''
        )

    assert inspect_(voice_1).is_well_formed()

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert inspect_(voice_2).is_well_formed()


def test_scoretools_Container_extend_09():
    r'''Extend container with LilyPond input string.
    '''

    container = Container([])
    container.extend("c'4 ( d'4 e'4 f'4 )")

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'4 (
            d'4
            e'4
            f'4 )
        }
        '''
        )

    assert inspect_(container).is_well_formed()


def test_scoretools_Container_extend_10():
    r'''Selections are stripped out.
    '''

    selection_1 = scoretools.make_notes([0, 2], [Duration(1, 4)])
    selection_2 = scoretools.make_notes([4, 5], [Duration(1, 4)])
    selection_3 = scoretools.make_notes([7, 9], [Duration(1, 4)])
    selection_4 = scoretools.make_notes([11, 12], [Duration(1, 4)])
    selections = [selection_1, selection_2, selection_3, selection_4]
    container = Container()
    container.extend(selections)

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'4
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
        }
        '''
        )

    assert inspect_(container).is_well_formed()
