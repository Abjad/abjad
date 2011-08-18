from abjad import *


def test_gracetools_iterate_components_and_grace_containers_forward_in_expr_01():
    '''Yield before-gracenotes and after-gracenotes.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
    gracetools.Grace(notes[:2], kind = 'grace')(t[1])
    gracetools.Grace(notes[2:], kind = 'after')(t[1])

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

    notes = list(gracetools.iterate_components_and_grace_containers_forward_in_expr(t, Note))

    "[Note(c', 8), Note(c', 16), Note(d', 16), Note(d', 8), Note(e', 16), Note(f', 16), Note(e', 8), Note(f', 8)]"

    assert notes[0] is t[0]
    assert notes[1] is t[1].grace[0]
    assert notes[2] is t[1].grace[1]
    assert notes[3] is t[1]
    assert notes[4] is t[1].after_grace[0]
    assert notes[5] is t[1].after_grace[1]
    assert notes[6] is t[2]
    assert notes[7] is t[3]
