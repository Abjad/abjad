import abjad


def test_LilyPondParser__comments_01():

    target = abjad.Container([abjad.Note(0, (1, 4))])

    string = r"""
    { c'4 }
    % { d'4 }
    % { e'4 }"""  # NOTE: no newline should follow the final brace

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result)
