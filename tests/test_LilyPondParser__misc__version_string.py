import abjad


def test_LilyPondParser__misc__version_string_01():
    """
    Version strings are ignored.
    """

    target = abjad.Staff()
    string = r"""\version "2.14.2" \new Staff { }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
