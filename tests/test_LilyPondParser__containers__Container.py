import abjad


def test_LilyPondParser__containers__Container_01():
    parser = abjad.parser.LilyPondParser()
    target = abjad.Container()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
