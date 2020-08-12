import abjad


def test_get_markup_01():

    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup("UP", direction=abjad.Up)
    abjad.attach(up_markup, chord)
    down_markup = abjad.Markup("DOWN", direction=abjad.Down)
    abjad.attach(down_markup, chord)
    found_markup = abjad.get.markup(chord, direction=abjad.Down)
    assert found_markup == [down_markup]


def test_get_markup_02():

    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup("UP", direction=abjad.Up)
    abjad.attach(up_markup, chord)
    down_markup = abjad.Markup("DOWN", direction=abjad.Down)
    abjad.attach(down_markup, chord)
    found_markup = abjad.get.markup(chord, direction=abjad.Up)
    assert found_markup == [up_markup]
