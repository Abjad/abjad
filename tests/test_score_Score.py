import abjad


def test_Score_tag():
    """
    Scores may be tagged.
    """

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    score = abjad.Score([staff], tag=abjad.Tag("RED"))

    assert abjad.lilypond(score, tags=True) == abjad.string.normalize(
        r"""
          %! RED
        \new Score
          %! RED
        <<
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }
          %! RED
        >>
        """
    )
