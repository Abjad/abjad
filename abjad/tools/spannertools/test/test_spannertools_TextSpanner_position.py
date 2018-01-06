import abjad


def test_spannertools_TextSpanner_position_01():

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])
    command = abjad.LilyPondLiteral(r'\textSpannerNeutral')
    abjad.attach(command, text_spanner[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \textSpannerNeutral
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )


def test_spannertools_TextSpanner_position_02():

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])
    command = abjad.LilyPondLiteral(r'\textSpannerUp')
    abjad.attach(command, text_spanner[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \textSpannerUp
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )


def test_spannertools_TextSpanner_position_03():

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])
    command = abjad.LilyPondLiteral(r'\textSpannerDown')
    abjad.attach(command, text_spanner[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \textSpannerDown
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )
