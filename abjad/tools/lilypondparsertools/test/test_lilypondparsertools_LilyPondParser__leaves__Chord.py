import abjad


def test_lilypondparsertools_LilyPondParser__leaves__Chord_01():

    target = abjad.Chord([0, 1, 4], (1, 4))
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser('{ %s }' % format(target))
    assert format(target) == format(result[0]) and target is not result[0]
