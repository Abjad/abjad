import abjad


def test_LilyPondParser__containers__simultaneous_01():

    target = abjad.Container()
    target.simultaneous = True
    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
