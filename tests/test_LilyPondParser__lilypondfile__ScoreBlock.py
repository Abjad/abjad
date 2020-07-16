import abjad


def test_LilyPondParser__lilypondfile__ScoreBlock_01():

    target = abjad.Block(name="score")
    target.items.append(abjad.Score())
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
