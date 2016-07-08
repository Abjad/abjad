# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_duration_01():
    r'''Spanner duration in seconds equals sum of duration
    of all leaves in spanner, in seconds.
    '''

    voice = Voice([
        Measure((2, 12), "c'8 d'8", implicit_scaling=True),
        Measure((2, 8), "c'8 d'8")]
        )
    leaves = select(voice).by_leaf()
    tempo = Tempo(Duration(1, 8), 42)
    attach(tempo, voice, scope=Voice)
    beam = Beam()
    attach(beam, leaves)
    crescendo = Crescendo()
    attach(crescendo, voice[0][:])
    decrescendo = Decrescendo()
    attach(decrescendo, voice[1][:])

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(beam).get_duration(in_seconds=True) == Duration(100, 21)
    assert inspect_(crescendo).get_duration(in_seconds=True) == Duration(40, 21)
    assert inspect_(decrescendo).get_duration(in_seconds=True) == \
        Duration(20, 7)


def test_agenttools_InspectionAgent_get_duration_02():

    voice = Voice(
        [Measure((2, 12), "c'8 d'8", implicit_scaling=True),
        Measure((2, 8), "c'8 d'8")]
        )
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)
    crescendo = Crescendo()
    attach(crescendo, voice[0][:])
    decrescendo = Decrescendo()
    attach(decrescendo, voice[1][:])

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(beam).get_duration() == Duration(5, 12)
    assert inspect_(crescendo).get_duration() == Duration(2, 12)
    assert inspect_(decrescendo).get_duration() == Duration(2, 8)


def test_agenttools_InspectionAgent_get_duration_03():
    r'''Container duration in seconds equals
    sum of leaf durations in seconds.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = Tempo(Duration(1, 4), 38)
    attach(tempo, staff)
    tempo = Tempo(Duration(1, 4), 42)
    attach(tempo, staff[2])
    score = Score([staff])

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=38
                c'8
                d'8
                \tempo 4=42
                e'8
                f'8
            }
        >>
        '''
        )

    assert inspect_(score).get_duration(in_seconds=True) == Duration(400, 133)


def test_agenttools_InspectionAgent_get_duration_04():
    r'''Container can not calculate duration in seconds
    without tempo indication.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    statement = 'inspect_(container).get_duration(in_seconds=True)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_duration_05():
    r'''Clock duration equals duration divide by effective tempo.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = Tempo(Duration(1, 4), 38)
    attach(tempo, staff)
    tempo = Tempo(Duration(1, 4), 42)
    attach(tempo, staff[2])
    Score([staff])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \tempo 4=38
            c'8
            d'8
            \tempo 4=42
            e'8
            f'8
        }
        '''
        )

    assert inspect_(staff[0]).get_duration(in_seconds=True) == Duration(15, 19)
    assert inspect_(staff[1]).get_duration(in_seconds=True) == Duration(15, 19)
    assert inspect_(staff[2]).get_duration(in_seconds=True) == Duration(5, 7)
    assert inspect_(staff[3]).get_duration(in_seconds=True) == Duration(5, 7)


def test_agenttools_InspectionAgent_get_duration_06():
    r'''Clock duration can not calculate without tempo.
    '''

    note = Note("c'4")
    statement = 'inspect_(note).get_duration(in_seconds=True)'
    assert pytest.raises(Exception, statement)
