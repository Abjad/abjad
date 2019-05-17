import abjad


def test_LilyPondParser__leaves__Chord_01():

    target = abjad.Chord([0, 1, 4], (1, 4))
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % format(target))
    assert format(target) == format(result[0]) and target is not result[0]
