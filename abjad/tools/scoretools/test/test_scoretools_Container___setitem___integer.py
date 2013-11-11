# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Container___setitem___integer_01():
    r'''Spanned leaves exchange correctly.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])
    glissando = spannertools.Glissando()
    attach(glissando, voice.select_leaves())

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    voice[1] = Note(12, (1, 8))

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            c''8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_02():
    r'''Spanned leaf hands position over to container correctly.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])
    glissando = spannertools.Glissando()
    attach(glissando, voice.select_leaves())

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    voice[1] = Container(scoretools.make_repeated_notes(3, Duration(1, 16)))

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                c'16 \glissando
                c'16 \glissando
                c'16 ] \glissando
            }
            e'8 \glissando
            f'8
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_03():
    r'''Directly spanned contains hand over correctly to a single leaf.
    Note here that only the sequentials are initially spanned.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, voice[:])
    glissando = spannertools.Glissando()
    attach(glissando, voice[:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = Note(12, (1, 8))

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            c''8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_04():
    r'''Indirectly spanned containers hand over correctly to a single leaf.
    Notice here that only LEAVES are initially spanned.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, voice.select_leaves())
    glissando = spannertools.Glissando()
    attach(glissando, voice.select_leaves())

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = Note(12, (1, 8))

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            c''8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_05():
    r'''Directly spanned containers hand over to other containers correctly.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, voice[:])
    glissando = spannertools.Glissando()
    attach(glissando, voice[:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \times 2/3 {
                c'8 \glissando
                d'8 \glissando
                e'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_06():
    r'''Indirectly spanned containers hand over correctly to a single leaf.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, voice.select_leaves())
    glissando = spannertools.Glissando()
    attach(glissando, voice.select_leaves())

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = Note(12, (1, 8))

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            c''8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_07():
    r'''Indirectly HALF-spanned containers hand over correctly to a
    single leaf. WOW!'''

    voice = Voice(Container(scoretools.make_repeated_notes(4)) * 2)
    voice = Voice("{ c'8 d'8 e'8 f'8 } { g'8 a'8 b'8 c''8 }")
    beam = Beam()
    attach(beam, voice.select_leaves()[0:6])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
                b'8
                c''8
            }
        }
        '''
        )

    voice[1] = Rest((1, 2))

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
            r2
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_08():
    r'''Take spanned leaf from donor container
    and insert into recipient container.
    Both donor and recipient check after set item.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8")]

    voice = Voice(notes[:3])
    beam = Beam()
    attach(beam, voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    u = Voice(notes[3:])
    beam = Beam()
    attach(beam, u[:])

    r'''
    \new Voice {
        f'8 [
        g'8
        a'8 ]
    }
    '''

    voice[1] = u[1]

    "Modified voice:"

    r'''
    \new Voice {
        c'8 [
        g'8
        e'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            g'8
            e'8 ]
        }
        '''
        )

    "Modified u:"

    assert systemtools.TestManager.compare(
        u,
        r'''
        \new Voice {
            f'8 [
            a'8 ]
        }
        '''
        )

    assert inspect(u).is_well_formed()


def test_scoretools_Container___setitem___integer_09():
    r'''Take down-spanned container with completely covered spanner
    from donor container and insert into recipient container.
    Both donor and recipient check after set item.
    '''

    notes = [
        Note("c'8"), Note("d'8"), Note("e'8"), 
        Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"),
        ]
    voice = Voice(notes[:3])
    beam = Beam()
    attach(beam, voice[:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    u = Voice(notes[3:])
    Container(u[1:3])
    glissando = spannertools.Glissando()
    attach(glissando, u.select_leaves())
    slur = Slur()
    attach(slur, u[1].select_leaves())

    assert systemtools.TestManager.compare(
        u,
        r'''
        \new Voice {
            f'8 \glissando
            {
                g'8 \glissando (
                a'8 \glissando )
            }
            b'8
        }
        '''
        )

    voice[1] = u[1]

    "Voice voice is now ..."

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            {
                g'8 (
                a'8 )
            }
            e'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()

    "Voice u is now ..."

    assert inspect(u).is_well_formed()
    assert systemtools.TestManager.compare(
        u,
        r'''
        \new Voice {
            f'8 \glissando
            b'8
        }
        '''
        )
