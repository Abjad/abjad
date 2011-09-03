from abjad import *
from abjad.tools import verticalitytools


def test_verticalitytools_iterate_vertical_moments_backward_in_expr_01():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(3))]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff(notetools.make_repeated_notes(2, Duration(1, 4))))
    piano_staff.append(Staff(notetools.make_repeated_notes(4)))
    contexttools.ClefMark('bass')(piano_staff[1])
    score.append(piano_staff)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(list(reversed(score.leaves)))

    r'''
    \new Score <<
        \new Staff {
            \times 4/3 {
                d''8
                c''8
                b'8
            }
        }
        \new PianoStaff <<
            \new Staff {
                a'4
                g'4
            }
            \new Staff {
                \clef "bass"
                f'8
                e'8
                d'8
                c'8
            }
        >>
    >>
    '''

    moment_generator = verticalitytools.iterate_vertical_moments_backward_in_expr(score)
    moments = list(moment_generator)

    r'''
    (Note(b', 8), Note(g', 4), Note(c', 8))
    (Note(b', 8), Note(g', 4), Note(d', 8))
    (Note(c'', 8), Note(g', 4), Note(d', 8))
    (Note(c'', 8), Note(a', 4), Note(e', 8))
    (Note(d'', 8), Note(a', 4), Note(e', 8))
    (Note(d'', 8), Note(a', 4), Note(f', 8))
    '''

    tuplet = score[0][0].leaves
    treble = piano_staff[0].leaves
    bass = piano_staff[1].leaves

    assert moments[0].leaves == (tuplet[2], treble[1], bass[3])
    assert moments[1].leaves == (tuplet[2], treble[1], bass[2])
    assert moments[2].leaves == (tuplet[1], treble[1], bass[2])
    assert moments[3].leaves == (tuplet[1], treble[0], bass[1])
    assert moments[4].leaves == (tuplet[0], treble[0], bass[1])
    assert moments[5].leaves == (tuplet[0], treble[0], bass[0])


def test_verticalitytools_iterate_vertical_moments_backward_in_expr_02():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(3))]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff(notetools.make_repeated_notes(2, Duration(1, 4))))
    piano_staff.append(Staff(notetools.make_repeated_notes(4)))
    contexttools.ClefMark('bass')(piano_staff[1])
    score.append(piano_staff)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(list(reversed(score.leaves)))

    # see above for formatted score #

    moment_generator = verticalitytools.iterate_vertical_moments_backward_in_expr(piano_staff)
    moments = list(moment_generator)

    r'''
    (Note(g', 4), Note(c', 8))
    (Note(g', 4), Note(d', 8))
    (Note(a', 4), Note(e', 8))
    (Note(a', 4), Note(f', 8))
    '''

    treble = piano_staff[0].leaves
    bass = piano_staff[1].leaves

    assert moments[0].leaves == (treble[1], bass[3])
    assert moments[1].leaves == (treble[1], bass[2])
    assert moments[2].leaves == (treble[0], bass[1])
    assert moments[3].leaves == (treble[0], bass[0])
