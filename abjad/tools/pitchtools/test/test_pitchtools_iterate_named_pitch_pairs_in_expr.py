# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_iterate_named_pitch_pairs_in_expr_01():

    score = Score([])
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'4")]
    score.append(Staff(notes))
    notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
    score.append(Staff(notes))
    clef = Clef('bass')
    attach(clef, score[1])

    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'4
            }
            \new Staff {
                \clef "bass"
                c4
                a,4
                g,4
            }
        >>
        '''
        )

    pairs = pitchtools.iterate_named_pitch_pairs_in_expr(score)
    pairs = list(pairs)

    assert pairs[0] == (NamedPitch('c', 4), NamedPitch('c', 3)) #
    assert pairs[1] == (NamedPitch('c', 4), NamedPitch('d', 4))
    assert pairs[2] == (NamedPitch('c', 3), NamedPitch('d', 4))
    assert pairs[3] == (NamedPitch('d', 4), NamedPitch('e', 4))
    assert pairs[4] == (NamedPitch('d', 4), NamedPitch('a', 2))
    assert pairs[5] == (NamedPitch('c', 3), NamedPitch('e', 4))
    assert pairs[6] == (NamedPitch('c', 3), NamedPitch('a', 2))
    assert pairs[7] == (NamedPitch('e', 4), NamedPitch('a', 2))
    assert pairs[8] == (NamedPitch('e', 4), NamedPitch('f', 4))
    assert pairs[9] == (NamedPitch('a', 2), NamedPitch('f', 4))
    assert pairs[10] == (NamedPitch('f', 4), NamedPitch('g', 4))
    assert pairs[11] == (NamedPitch('f', 4), NamedPitch('g', 2))
    assert pairs[12] == (NamedPitch('a', 2), NamedPitch('g', 4))
    assert pairs[13] == (NamedPitch('a', 2), NamedPitch('g', 2))
    assert pairs[14] == (NamedPitch('g', 4), NamedPitch('g', 2))


def test_pitchtools_iterate_named_pitch_pairs_in_expr_02():

    chord_1 = Chord([0, 2, 4], (1, 4))
    chord_2 = Chord([17, 19], (1, 4))
    staff = Staff([chord_1, chord_2])

    r'''
    \new Staff {
        <c' d' e'>4
        <f'' g''>4
    }
    '''

    pairs = pitchtools.iterate_named_pitch_pairs_in_expr(staff)
    pairs = list(pairs)

    assert pairs[0] == (NamedPitch('c', 4), NamedPitch('d', 4))
    assert pairs[1] == (NamedPitch('c', 4), NamedPitch('e', 4))
    assert pairs[2] == (NamedPitch('d', 4), NamedPitch('e', 4))
    assert pairs[3] == (NamedPitch('c', 4), NamedPitch('f', 5))
    assert pairs[4] == (NamedPitch('c', 4), NamedPitch('g', 5))
    assert pairs[5] == (NamedPitch('d', 4), NamedPitch('f', 5))
    assert pairs[6] == (NamedPitch('d', 4), NamedPitch('g', 5))
    assert pairs[7] == (NamedPitch('e', 4), NamedPitch('f', 5))
    assert pairs[8] == (NamedPitch('e', 4), NamedPitch('g', 5))
    assert pairs[9] == (NamedPitch('f', 5), NamedPitch('g', 5))