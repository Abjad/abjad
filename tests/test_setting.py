import abjad


def test_setting_01():
    r"""
    Works with score metronome mark interface.

    Does not include LilyPond \set command.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    abjad.setting(score).tempoWholesPerMinute = r"\musicLength 1*24"

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        \with
        {
            tempoWholesPerMinute = \musicLength 1*24
        }
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )


def test_setting_02():
    r"""
    Works with leaf metronome mark interface.

    Includes LilyPond \set command.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    leaves = abjad.select.leaves(score)
    abjad.setting(leaves[1]).Score.tempoWholesPerMinute = r"\musicLength 1*24"

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                \set Score.tempoWholesPerMinute = \musicLength 1*24
                d'8
                e'8
                f'8
            }
        >>
        """
    )
