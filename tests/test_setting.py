import abjad


def test_setting_01():
    r"""
    Works with score metronome mark interface.

    Does not include LilyPond \set command.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    abjad.setting(score).tempo_wholes_per_minute = "#(ly:make-moment 24 1)"

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            tempoWholesPerMinute = #(ly:make-moment 24 1)
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
    leaves = abjad.select(score).leaves()
    abjad.setting(leaves[1]).score.tempo_wholes_per_minute = "#(ly:make-moment 24 1)"

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                \set Score.tempoWholesPerMinute = #(ly:make-moment 24 1)
                d'8
                e'8
                f'8
            }
        >>
        """
    )
