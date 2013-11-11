from abjad import *


def test_spannertools_TextSpanner__make_storage_format_with_overrides_01():

    text_spanner_1 = spannertools.TextSpanner()
    override(text_spanner_1).text_spanner.color = 'red'
    override(text_spanner_1).text_spanner.dash_fraction = 0.5

    staff_1 = Staff("c'8 d'8 e'8 f'8")
    attach(text_spanner_1, staff_1[:])

    assert systemtools.TestManager.compare(
        staff_1,
        r'''
        \new Staff {
            \override TextSpanner #'color = #red
            \override TextSpanner #'dash-fraction = #0.5
            c'8 \startTextSpan
            d'8
            e'8
            f'8 \stopTextSpan
            \revert TextSpanner #'color
            \revert TextSpanner #'dash-fraction
        }
        '''
        )

    string = text_spanner_1._make_storage_format_with_overrides()
    text_spanner_2 = eval(string)

    staff_2 = Staff("c'8 d'8 e'8 f'8")
    attach(text_spanner_2, staff_2[:])

    assert override(text_spanner_1) == override(text_spanner_2)
    assert format(staff_1) == format(staff_2)
