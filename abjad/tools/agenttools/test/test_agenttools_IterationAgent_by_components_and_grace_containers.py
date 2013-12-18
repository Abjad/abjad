# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_components_and_grace_containers_01():
    r'''Yield before-grace notes and after-grace notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
    grace = scoretools.GraceContainer(notes[:2], kind='grace')
    attach(grace, voice[1])
    after_grace = scoretools.GraceContainer(notes[2:], kind='after')
    attach(after_grace, voice[1])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \grace {
                c'16
                d'16
            }
            \afterGrace
            d'8
            {
                e'16
                f'16
            }
            e'8
            f'8 ]
        }
        ''',
        )

    notes = iterate(voice).by_components_and_grace_containers(Note)
    notes = list(notes)

    assert notes[0] is voice[0]
    assert notes[1] is grace[0]
    assert notes[2] is grace[1]
    assert notes[3] is voice[1]
    assert notes[4] is after_grace[0]
    assert notes[5] is after_grace[1]
    assert notes[6] is voice[2]
    assert notes[7] is voice[3]
