from abjad import *
from abjad.tools import durationtools
from abjad.tools import verticalitytools


def test_VerticalMoment_prev_vertical_moment_01():

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

    last_leaf = score.leaves[-1]
    vertical_moment = verticalitytools.get_vertical_moment_starting_with_component(last_leaf)
    assert vertical_moment.prolated_offset == durationtools.Offset(3, 8)

    vertical_moment = vertical_moment.prev_vertical_moment
    assert vertical_moment.prolated_offset == durationtools.Offset(1, 3)

    vertical_moment = vertical_moment.prev_vertical_moment
    assert vertical_moment.prolated_offset == durationtools.Offset(1, 4)

    vertical_moment = vertical_moment.prev_vertical_moment
    assert vertical_moment.prolated_offset == durationtools.Offset(1, 6)

    vertical_moment = vertical_moment.prev_vertical_moment
    assert vertical_moment.prolated_offset == durationtools.Offset(1, 8)

    vertical_moment = vertical_moment.prev_vertical_moment
    assert vertical_moment.prolated_offset == durationtools.Offset(0)
