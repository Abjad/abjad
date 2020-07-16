import abjad


def test_LilyPondParser__contexts__Score_01():

    target = abjad.Score()

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Score
        <<
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
