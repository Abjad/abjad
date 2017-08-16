import abjad


def test_scoretools_Tuplet_timespan_01():

    staff = abjad.Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4
            d'4
            \times 2/3 {
                e'4
                f'4
                g'4
            }
        }
        '''
        )

    assert abjad.inspect(staff).get_timespan() == abjad.Timespan(0, 1)
    assert abjad.inspect(staff[0]).get_timespan() == abjad.Timespan(0, (1, 4))
    assert abjad.inspect(staff[1]).get_timespan() == abjad.Timespan((1, 4), (1, 2))
    assert abjad.inspect(staff[-1]).get_timespan() == abjad.Timespan((1, 2), 1)
