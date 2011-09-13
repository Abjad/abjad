from abjad import *


def test_notetools_iterate_notes_backward_in_expr_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    generator = notetools.iterate_notes_backward_in_expr(staff)
    notes = list(generator)

    assert notes[0] is staff[2][1]
    assert notes[1] is staff[2][0]
    assert notes[2] is staff[1][1]
    assert notes[3] is staff[1][0]
    assert notes[4] is staff[0][1]
    assert notes[5] is staff[0][0]


def test_notetools_iterate_notes_backward_in_expr_02():
    '''Optional start and stop keyword parameters.'''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    notes = list(notetools.iterate_notes_backward_in_expr(staff, start = 3))
    assert notes[0] is staff[1][0]
    assert notes[1] is staff[0][1]
    assert notes[2] is staff[0][0]
    assert len(notes) == 3

    notes = list(notetools.iterate_notes_backward_in_expr(staff, start = 0, stop = 3))
    assert notes[0] is staff[2][1]
    assert notes[1] is staff[2][0]
    assert notes[2] is staff[1][1]
    assert len(notes) == 3

    notes = list(notetools.iterate_notes_backward_in_expr(staff, start = 2, stop = 4))
    assert notes[0] is staff[1][1]
    assert notes[1] is staff[1][0]
    assert len(notes) == 2
