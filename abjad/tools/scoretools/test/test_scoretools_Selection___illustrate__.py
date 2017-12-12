import abjad


def test_scoretools_Selection___illustrate___01():

    staff = abjad.Staff("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    selection = staff[2:6]
    lilypond_file = selection.__illustrate__()
    score = lilypond_file[abjad.Score]

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                e'4
                f'4
                g'4
                a'4
            }
        >>
        '''
        )


def test_scoretools_Selection___illustrate___02():

    staff = abjad.Staff("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    abjad.attach(abjad.Slur(), staff[:])
    selection = staff[2:6]
    lilypond_file = selection.__illustrate__()
    score = lilypond_file[abjad.Score]

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                e'4 (
                f'4
                g'4
                a'4 )
            }
        >>
        '''
        )
