from abjad import *
from abjad.tools import durationtools
from abjad.tools import verticalitytools


def test_verticalitytools_get_vertical_moment_at_prolated_offset_in_expr_01():

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

    def piano_staff_moment(prolated_offset):
        return verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
            piano_staff, prolated_offset)

    vm = piano_staff_moment(durationtools.Offset(0, 8))
    assert vm.leaves == (piano_staff[0][0], piano_staff[1][0])

    vm = piano_staff_moment(durationtools.Offset(1, 8))
    assert vm.leaves == (piano_staff[0][0], piano_staff[1][1])

    vm = piano_staff_moment(durationtools.Offset(2, 8))
    assert vm.leaves == (piano_staff[0][1], piano_staff[1][2])

    vm = piano_staff_moment(durationtools.Offset(3, 8))
    assert vm.leaves == (piano_staff[0][1], piano_staff[1][3])

    vm = piano_staff_moment(durationtools.Offset(99, 8))
    assert vm.leaves == ()


def test_verticalitytools_get_vertical_moment_at_prolated_offset_in_expr_02():

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

    def scorewide_vertical_moment(prolated_offset):
        return verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
            score, prolated_offset)

    vm = scorewide_vertical_moment(durationtools.Offset(0, 8))
    assert vm.leaves == (score[0][0][0], piano_staff[0][0], piano_staff[1][0])

    vm = scorewide_vertical_moment(durationtools.Offset(1, 8))
    assert vm.leaves == (score[0][0][0], piano_staff[0][0], piano_staff[1][1])

    vm = scorewide_vertical_moment(durationtools.Offset(2, 8))
    assert vm.leaves == (score[0][0][1], piano_staff[0][1], piano_staff[1][2])

    vm = scorewide_vertical_moment(durationtools.Offset(3, 8))
    assert vm.leaves == (score[0][0][2], piano_staff[0][1], piano_staff[1][3])

    vm = scorewide_vertical_moment(durationtools.Offset(99, 8))
    assert vm.leaves == ()
