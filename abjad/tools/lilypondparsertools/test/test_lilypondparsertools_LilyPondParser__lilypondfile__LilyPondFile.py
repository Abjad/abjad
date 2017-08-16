import abjad


def test_lilypondparsertools_LilyPondParser__lilypondfile__LilyPondFile_01():

    string = '{ c } { c } { c } { c }'
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert isinstance(result, abjad.LilyPondFile)
