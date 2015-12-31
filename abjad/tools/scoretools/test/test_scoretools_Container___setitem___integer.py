# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Container___setitem___integer_01():
    r'''Replaces in-score leaf with out-of-score leaf.
    '''

    voice = Voice("c'8 [ d'8 ] e'8 f'8")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))

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

    voice[1] = Note("c''8")

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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_02():
    r'''Replaces in-score leaf with out-of-score container.
    '''

    voice = Voice("c'8 [ d'8 ] e'8 f'8")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    glissando = Glissando(allow_repeated_pitches=True)
    attach(glissando, list(leaves))

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

    voice[1] = Container("c'16 c'16 c'16")

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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_03():
    r'''Replaces in-score container with out-of-score leaf.
    '''

    voice = Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))

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

    voice[1] = Note("c''8")

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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_04():
    r'''Replaces in-score container with out-of-score tuplet.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    attach(Beam(), voice[:])
    attach(Glissando(), voice[:])

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

    voice[1] = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_05():
    r'''Replaces in-score container with out-of-score leaf.
    '''

    voice = Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))

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

    voice[1] = Note("c''8")

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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_06():
    r'''Replaces in-score container with out-of-score leaf.
    '''

    voice = Voice(2 * Container("c'8 c'8 c'8 c'8"))
    voice = Voice("{ c'8 d'8 e'8 f'8 } { g'8 a'8 b'8 c''8 }")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Beam(), list(leaves)[0:6])

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

    voice[1] = Rest('r2')

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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___integer_07():
    r'''Replaces note in one score with note from another score.
    '''

    notes = [
        Note("c'8"), Note("d'8"), Note("e'8"), 
        Note("f'8"), Note("g'8"), Note("a'8"),
        ]

    voice_1 = Voice(notes[:3])
    attach(Beam(), voice_1[:])

    assert systemtools.TestManager.compare(
        voice_1,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    voice_2 = Voice(notes[3:])
    attach(Beam(), voice_2[:])

    assert systemtools.TestManager.compare(
        voice_2,
        r'''
        \new Voice {
            f'8 [
            g'8
            a'8 ]
        }
        '''
        )

    voice_1[1] = voice_2[1]

    assert systemtools.TestManager.compare(
        voice_1,
        r'''
        \new Voice {
            c'8 [
            g'8
            e'8 ]
        }
        '''
        )

    assert inspect_(voice_1).is_well_formed()

    assert systemtools.TestManager.compare(
        voice_2,
        r'''
        \new Voice {
            f'8 [
            a'8 ]
        }
        '''
        )

    assert inspect_(voice_2).is_well_formed()


def test_scoretools_Container___setitem___integer_08():
    r'''Replaces note in one score with container from another score.
    '''

    notes = [
        Note("c'8"), Note("d'8"), Note("e'8"),
        Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"),
        ]
    voice_1 = Voice(notes[:3])
    attach(Beam(), voice_1[:])

    assert systemtools.TestManager.compare(
        voice_1,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    voice_2 = Voice(notes[3:])
    Container(voice_2[1:3])
    leaves = iterate(voice_2).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))
    leaves = iterate(voice_2[1]).by_class(scoretools.Leaf)
    attach(Slur(), list(leaves))

    assert systemtools.TestManager.compare(
        voice_2,
        r'''
        \new Voice {
            f'8 \glissando
            {
                g'8 \glissando (
                a'8 ) \glissando
            }
            b'8
        }
        '''
        )

    voice_1[1] = voice_2[1]

    assert systemtools.TestManager.compare(
        voice_1,
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

    assert inspect_(voice_1).is_well_formed()

    assert systemtools.TestManager.compare(
        voice_2,
        r'''
        \new Voice {
            f'8 \glissando
            b'8
        }
        '''
        )

    assert inspect_(voice_2).is_well_formed()