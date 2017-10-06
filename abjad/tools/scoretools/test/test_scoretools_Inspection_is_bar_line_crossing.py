import abjad


def test_scoretools_Inspection_is_bar_line_crossing_01():
    r'''Works with partial.
    '''

    staff = abjad.Staff("c'8 d'8 e'4 f'8")
    time_signature = abjad.TimeSignature((2, 8), partial=abjad.Duration(1, 8))
    abjad.attach(time_signature, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \partial 8
            \time 2/8
            c'8
            d'8
            e'4
            f'8
        }
        '''
        )

    assert not abjad.inspect(staff[0]).is_bar_line_crossing()
    assert not abjad.inspect(staff[1]).is_bar_line_crossing()
    assert abjad.inspect(staff[2]).is_bar_line_crossing()
    assert not abjad.inspect(staff[3]).is_bar_line_crossing()


def test_scoretools_Inspection_is_bar_line_crossing_02():
    r'''Works when no explicit time signature is abjad.attached.
    '''

    staff = abjad.Staff("c'2 d'1 e'2")

    assert not abjad.inspect(staff[0]).is_bar_line_crossing()
    assert abjad.inspect(staff[1]).is_bar_line_crossing()
    assert not abjad.inspect(staff[2]).is_bar_line_crossing()
