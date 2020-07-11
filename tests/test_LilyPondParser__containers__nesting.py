import abjad


def test_LilyPondParser__containers__nesting_01():

    target = abjad.Container(
        [abjad.Container([]), abjad.Container([abjad.Container([])])]
    )

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        {
            {
            }
            {
                {
                }
            }
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
