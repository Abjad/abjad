import abjad


def test_LilyPondParser__indicators__Clef_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    clef = abjad.Clef("bass")
    abjad.attach(clef, target[0])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "bass"
            c'1
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    clefs = abjad.get.indicators(result[0], abjad.Clef)
    assert len(clefs) == 1
