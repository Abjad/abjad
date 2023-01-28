import abjad


def test_LilyPondParser_accidentals_forced_01():
    string = "{ c!4 }"
    parsed = abjad.parser.LilyPondParser()(string)

    assert parsed[0].note_head.is_forced is True
    assert abjad.lilypond(parsed[0]) == "c!4"


def test_LilyPondParser_accidentals_forced_02():
    string = "{ <c! e g!!>4 }"
    parsed = abjad.parser.LilyPondParser()(string)

    assert parsed[0].note_heads[0].is_forced is True
    assert parsed[0].note_heads[1].is_forced is False
    assert parsed[0].note_heads[2].is_forced is True
    assert abjad.lilypond(parsed[0]) == "<c! e g!>4"
