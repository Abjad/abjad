# -*- encoding: utf-8 -*-
from abjad import *


def test_VerticalMoment_previous_vertical_moment_01():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(
        Duration(4, 8), notetools.make_repeated_notes(3))]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff(notetools.make_repeated_notes(2, Duration(1, 4))))
    piano_staff.append(Staff(notetools.make_repeated_notes(4)))
    contexttools.ClefMark('bass')(piano_staff[1])
    score.append(piano_staff)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        list(reversed(score.select_leaves(allow_discontiguous_leaves=True))))

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

    last_leaf = score.select_leaves(allow_discontiguous_leaves=True)[-1]
    vertical_moment = more(last_leaf).select_vertical_moment()
    assert vertical_moment.offset == Offset(3, 8)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 3)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 4)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 6)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 8)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(0)
