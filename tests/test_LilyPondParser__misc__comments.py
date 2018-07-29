import abjad


def test_LilyPondParser__misc__comments_01():
    """
    Comments are ignored.
    """

    target = abjad.Staff()
    string = r"""\new Staff { %{ HOO HAH %} }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
