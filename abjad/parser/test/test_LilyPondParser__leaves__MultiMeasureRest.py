import abjad


def test_LilyPondParser__leaves__MultiMeasureRest_01():

    target = abjad.MultimeasureRest((1, 4))
    parser = abjad.parser.LilyPondParser()
    result = parser('{ %s }' % format(target))
    assert format(target) == format(result[0]) and target is not result[0]
