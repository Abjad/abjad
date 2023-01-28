import abjad


def test_LilyPondParser__lilypondfile__LilyPondFile_01():
    string = "{ c } { c } { c } { c }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert isinstance(result, abjad.LilyPondFile)
