import abjad


def test_LilyPondParser__containers__simultaneous_01():
    target = abjad.Container()
    target.simultaneous = True
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
