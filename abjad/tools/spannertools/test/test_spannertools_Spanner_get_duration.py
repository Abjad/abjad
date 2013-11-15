# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_spannertools_Spanner_get_duration_01():
    r'''Spanner duration in seconds equals sum of duration
    of all leaves in spanner, in seconds.
    '''

    voice = Voice([
        Measure((2, 12), "c'8 d'8"),
        Measure((2, 8), "c'8 d'8")]
        )
    tempo = Tempo(Duration(1, 8), 42)
    attach(tempo, voice, scope=Voice)
    beam = Beam()
    attach(beam, voice.select_leaves())
    crescendo = Crescendo()
    attach(crescendo, voice[0][:])
    decrescendo = Decrescendo()
    attach(decrescendo, voice[1][:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            \tempo 8=42
            {
                \time 2/12
                \scaleDurations #'(2 . 3) {
                    c'8 [ \<
                    d'8 \!
                }
            }
            {
                \time 2/8
                c'8 \>
                d'8 ] \!
            }
        }
        '''
        )

    assert beam.get_duration(in_seconds=True) == Duration(100, 21)
    assert crescendo.get_duration(in_seconds=True) == Duration(40, 21)
    assert decrescendo.get_duration(in_seconds=True) == Duration(20, 7)


def test_spannertools_Spanner_get_duration_02():

    voice = Voice(
        [Measure((2, 12), "c'8 d'8"),
        Measure((2, 8), "c'8 d'8")]
        )
    beam = Beam()
    attach(beam, voice.select_leaves())
    crescendo = Crescendo()
    attach(crescendo, voice[0][:])
    decrescendo = Decrescendo()
    attach(decrescendo, voice[1][:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/12
                \scaleDurations #'(2 . 3) {
                    c'8 [ \<
                    d'8 \!
                }
            }
            {
                \time 2/8
                c'8 \>
                d'8 ] \!
            }
        }
        '''
        )

    assert beam.get_duration() == Duration(5, 12)
    assert crescendo.get_duration() == Duration(2, 12)
    assert decrescendo.get_duration() == Duration(2, 8)
