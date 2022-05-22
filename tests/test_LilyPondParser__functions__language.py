import abjad


def test_LilyPondParser__functions__language_01():

    target = abjad.Container(
        [abjad.Note("cs'8"), abjad.Note("ds'8"), abjad.Note("ff'8")]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            cs'8
            ds'8
            ff'8
        }
        """
    )

    string = r"\language nederlands { cis'8 dis'8 fes'8 }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
