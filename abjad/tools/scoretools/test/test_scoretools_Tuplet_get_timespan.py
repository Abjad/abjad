# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Tuplet_get_timespan_01():

    staff = abjad.Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")
    leaves = abjad.select(staff).by_leaf()
    score = abjad.Score([staff])
    mark = abjad.MetronomeMark((1, 4), 60)
    abjad.attach(mark, leaves[0])

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=60
                c'4
                d'4
                \times 2/3 {
                    e'4
                    f'4
                    g'4
                }
            }
        >>
        '''
        )

    assert abjad.inspect(staff).get_timespan(in_seconds=True) == \
        abjad.Timespan(0, 4)
    assert abjad.inspect(staff[0]).get_timespan(in_seconds=True) == \
        abjad.Timespan(0, 1)
    assert abjad.inspect(staff[1]).get_timespan(in_seconds=True) == \
        abjad.Timespan(1, 2)
    assert abjad.inspect(staff[-1]).get_timespan(in_seconds=True) == \
        abjad.Timespan(2, 4)
