# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_components_and_grace_containers_in_expr_01():
    r'''Yield before-gracenotes and after-gracenotes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
    scoretools.GraceContainer(notes[:2], kind='grace')(voice[1])
    scoretools.GraceContainer(notes[2:], kind='after')(voice[1])

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
    '''

    notes = list(iterationtools.iterate_components_and_grace_containers_in_expr(voice, Note))

    "[Note(c', 8), Note(c', 16), Note(d', 16), Note(d', 8), Note(e', 16), Note(f', 16), Note(e', 8), Note(f', 8)]"

    assert notes[0] is voice[0]
    assert notes[1] is voice[1].grace[0]
    assert notes[2] is voice[1].grace[1]
    assert notes[3] is voice[1]
    assert notes[4] is voice[1].after_grace[0]
    assert notes[5] is voice[1].after_grace[1]
    assert notes[6] is voice[2]
    assert notes[7] is voice[3]
