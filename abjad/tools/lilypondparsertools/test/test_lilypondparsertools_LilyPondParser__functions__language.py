import abjad


def test_lilypondparsertools_LilyPondParser__functions__language_01():

    target = abjad.Container([
        abjad.Note("cs'8"),
        abjad.Note("ds'8"),
        abjad.Note("ff'8")
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            cs'8
            ds'8
            ff'8
        }
        '''
        )

    string = r"\language nederlands { cis'8 dis'8 fes'8 }"
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
