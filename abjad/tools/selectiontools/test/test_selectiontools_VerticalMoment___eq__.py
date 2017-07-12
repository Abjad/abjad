# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_VerticalMoment___eq___01():

    score = abjad.Score(
        r'''
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
        '''
        )

    staff_group = score[1]

    vertical_moment_1 = abjad.inspect(staff_group).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, abjad.Staff{2}, a'4, abjad.Staff{4}, e'8)"

    vertical_moment_2 = abjad.inspect(staff_group).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, abjad.Staff{2}, a'4, abjad.Staff{4}, e'8)"

    assert vertical_moment_1 == vertical_moment_2
    assert not vertical_moment_1 != vertical_moment_2


def test_selectiontools_VerticalMoment___eq___02():

    score = abjad.Score([])
    score.append(abjad.Staff([abjad.Tuplet((4, 3), "d''8 c''8 b'8")]))
    staff_group = abjad.StaffGroup(r'''
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
        '''
        )
    staff_group.context_name = 'PianoStaff'
    score.append(staff_group)

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
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
        )

    vertical_moment_1 = abjad.inspect(
        staff_group).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, abjad.Staff{2}, a'4, abjad.Staff{4}, e'8)"

    vertical_moment_2 = abjad.inspect(
        staff_group[0]).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(abjad.Staff{2}, a'4, abjad.Staff{4}, e'8)"

    assert not vertical_moment_1 == vertical_moment_2
    assert vertical_moment_1 != vertical_moment_2
