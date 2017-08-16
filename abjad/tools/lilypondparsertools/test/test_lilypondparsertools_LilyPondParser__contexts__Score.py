import abjad


def test_lilypondparsertools_LilyPondParser__contexts__Score_01():

    target = abjad.Score()

    assert format(target) == abjad.String.normalize(
        r'''
        \new Score <<
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
