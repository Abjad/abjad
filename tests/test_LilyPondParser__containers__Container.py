import abjad


def test_LilyPondParser__containers__Container_01():
    parser = abjad.parser.LilyPondParser()
    target = abjad.Container()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
