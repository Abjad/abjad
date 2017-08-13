import abjad


def test_lilypondparsertools_LilyPondParser__containers__simultaneous_01():

    target = abjad.Container()
    target.is_simultaneous = True
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
