import abjad


def test_lilypondparsertools_LilyPondParser__contexts__StaffGroup_01():

    target = abjad.StaffGroup([])

    assert format(target) == abjad.String.normalize(
        r'''
        \new StaffGroup <<
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
