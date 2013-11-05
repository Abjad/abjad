# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Container_append_01():
    r'''Append sequential to voice.
    '''

    voice = Voice("c'8 d'8")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])
    voice.append(Container("e'8 f'8"))

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            {
                e'8
                f'8
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container_append_02():
    r'''Append leaf to tuplet.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    beam = spannertools.BeamSpanner()
    attach(beam, tuplet[:])
    tuplet.append(Note(5, (1, 16)))

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/7 {
            c'8 [
            d'8
            e'8 ]
            f'16
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_scoretools_Container_append_03():
    r'''Trying to append noncomponent to container raises TypeError.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    assert pytest.raises(Exception, "voice.append('foo')")
    assert pytest.raises(Exception, "voice.append(99)")
    assert pytest.raises(Exception, "voice.append([])")
    assert pytest.raises(Exception, "voice.append([Note(0, (1, 8))])")


def test_scoretools_Container_append_04():
    r'''Append spanned leaf from donor container to recipient container.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    u = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    attach(beam, u[:])

    assert testtools.compare(
        u,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    voice.append(u[-1])

    "Container voice is now ..."

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
            f'8
        }
        '''
        )

    assert inspect(voice).is_well_formed()

    "Container u is now ..."

    assert testtools.compare(
        u,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert inspect(u).is_well_formed()


def test_scoretools_Container_append_05():
    r'''Append spanned leaf from donor container to recipient container.
    Donor and recipient containers are the same.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    voice.append(voice[1])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            e'8
            f'8 ]
            d'8
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container_append_06():
    r'''Can not insert grace container into container.
    '''

    staff = Staff("c' d' e'")
    grace_container = scoretools.GraceContainer("f'16 g'")

    assert pytest.raises(Exception, 'staff.append(grace_container)')
