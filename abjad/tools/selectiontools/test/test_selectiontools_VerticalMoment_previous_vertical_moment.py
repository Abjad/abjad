# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_VerticalMoment_previous_vertical_moment_01():

    score = abjad.Score(r'''
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
        ''')

    selector = abjad.select().by_leaf(flatten=True)
    leaves = selector(score)
    last_leaf = leaves[-1]
    vertical_moment = abjad.inspect(last_leaf).get_vertical_moment()
    assert vertical_moment.offset == abjad.Offset(3, 8)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 3)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 4)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 6)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 8)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == abjad.Offset(0)