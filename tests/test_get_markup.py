import abjad


def test_get_markup_01():

    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup(r"\markup UP")
    abjad.attach(up_markup, chord, direction=abjad.UP)
    down_markup = abjad.Markup(r"\markup DOWN")
    abjad.attach(down_markup, chord, direction=abjad.DOWN)
    found_markup = abjad.get.markup(chord, direction=abjad.DOWN)
    assert found_markup == [down_markup]


def test_get_markup_02():

    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup(r"\markup UP")
    abjad.attach(up_markup, chord, direction=abjad.UP)
    down_markup = abjad.Markup(r"\markup DOWN")
    abjad.attach(down_markup, chord, direction=abjad.DOWN)
    found_markup = abjad.get.markup(chord, direction=abjad.UP)
    assert found_markup == [up_markup]
