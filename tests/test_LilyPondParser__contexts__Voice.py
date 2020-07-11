import abjad


def test_LilyPondParser__contexts__Voice_01():

    target = abjad.Voice([])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Voice
        {
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
