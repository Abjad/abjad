import abjad


def test_LilyPondParser_accidentals_cautionary_01():

    string = "{ c?4 }"
    parsed = abjad.parser.LilyPondParser()(string)

    assert parsed[0].note_head.is_cautionary is True
    assert abjad.lilypond(parsed[0]) == "c?4"


def test_LilyPondParser_accidentals_cautionary_02():

    string = "{ <c? e g??>4 }"
    parsed = abjad.parser.LilyPondParser()(string)

    assert parsed[0].note_heads[0].is_cautionary is True
    assert parsed[0].note_heads[1].is_cautionary is False
    assert parsed[0].note_heads[2].is_cautionary is True
    assert abjad.lilypond(parsed[0]) == "<c? e g?>4"
