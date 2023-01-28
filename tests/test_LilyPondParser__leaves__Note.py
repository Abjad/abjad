import abjad


def test_LilyPondParser__leaves__Note_01():
    target = abjad.Note(0, 1)
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % abjad.lilypond(target))
    assert (
        abjad.lilypond(target) == abjad.lilypond(result[0]) and target is not result[0]
    )
