# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_Container_extend_01():
    r'''Extend container with list of leaves.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    voice.extend([Note("c'8"), Note("d'8")])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        c'8
        d'8
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            c'8
            d'8
        }
        '''
        )


def test_Container_extend_02():
    r'''Extend container with contents of other container.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    u = Voice([Note(4, (1, 8)), Note(5, (1, 8))])
    beam = spannertools.BeamSpanner()
    beam.attach(u[:])
    voice.extend(u)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8 [
        f'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
        }
        '''
        )


def test_Container_extend_03():
    r'''Extending container with empty list leaves container unchanged.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    voice.extend([])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )


def test_Container_extend_04():
    r'''Extending one container with empty second container leaves both containers unchanged.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    voice.extend(Voice([]))

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )


def test_Container_extend_05():
    r'''Trying to extend container with noncomponent raises TypeError.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    assert py.test.raises(Exception, 'voice.extend(7)')
    assert py.test.raises(Exception, "voice.extend('foo')")


def test_Container_extend_06():
    r'''Trying to extend container with noncontainer raises exception.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    assert py.test.raises(Exception, 'voice.extend(Note(4, (1, 4)))')
    assert py.test.raises(AssertionError, "voice.extend(Chord([2, 3, 5], (1, 4)))")


def test_Container_extend_07():
    r'''Extend container with partial and spanned contents of other container.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    u = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(u[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    voice.extend(u[-2:])

    "Container voice is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8
        f'8
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    "Container u is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert inspect(u).is_well_formed()
    assert testtools.compare(
        u,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )


def test_Container_extend_08():
    r'''Extend container with partial and spanned contents of other container.
    Covered span comes with components from donor container.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    u = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(u[:])
    slur = spannertools.SlurSpanner()
    slur.attach(u[-2:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 (
        f'8 ] )
    }
    '''

    voice.extend(u[-2:])

    "Container voice is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8 (
        f'8 )
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8 (
            f'8 )
        }
        '''
        )

    "Container u is now ..."

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert inspect(u).is_well_formed()
    assert testtools.compare(
        u,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )


def test_Container_extend_09():
    r'''Extend container with LilyPond input string.
    '''

    container = Container([])
    container.extend("c'4 ( d'4 e'4 f'4 )")

    r'''
    {
        c'4 (
        d'4
        e'4
        f'4 )
    }
    '''

    assert inspect(container).is_well_formed()
    assert testtools.compare(
        container,
        r'''
        {
            c'4 (
            d'4
            e'4
            f'4 )
        }
        '''
        )
