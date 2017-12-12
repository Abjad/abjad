import abjad


def test_scoretools_VerticalMoment___len___01():

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

    vertical_moment = abjad.inspect(score).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(abjad.Score<<2>>, abjad.Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8, PianoStaff<<2>>, abjad.Staff{2}, a'4, abjad.Staff{4}, e'8)"
    assert len(vertical_moment) == 9

    vertical_moment = abjad.inspect(score[0]).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(abjad.Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8)"
    assert len(vertical_moment) == 3

    vertical_moment = abjad.inspect(staff_group).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, abjad.Staff{2}, a'4, abjad.Staff{4}, e'8)"
    assert len(vertical_moment) == 5

    vertical_moment = abjad.inspect(staff_group[0]).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(abjad.Staff{2}, a'4)"
    assert len(vertical_moment) == 2

    vertical_moment = abjad.inspect(staff_group[1]).get_vertical_moment_at(abjad.Offset(1, 8))
    "VerticalMoment(abjad.Staff{2}, e'8)"
    assert len(vertical_moment) == 2
