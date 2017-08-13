import abjad


def test_lilypondparsertools_LilyPondParser__misc__comments_01():
    r'''Comments are ignored.
    '''

    target = abjad.Staff()
    string = r'''\new Staff { %{ HOO HAH %} }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
