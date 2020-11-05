import copy

import abjad


def test_Chord___copy___01():

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, abjad.Chord)
    assert isinstance(chord_2, abjad.Chord)
    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2


def test_Chord___copy___02():
    """
    Chord copies LilyPond duration multiplier.
    """

    chord_1 = abjad.Chord("<ef' cs'' f''>4 * 1/2")
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, abjad.Chord)
    assert isinstance(chord_2, abjad.Chord)
    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2


def test_Chord___copy___03():
    """
    Chord copies LilyPond grob overrides and LilyPond context settings.
    """

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    abjad.override(chord_1).staff.note_head.color = "red"
    abjad.override(chord_1).accidental.color = "red"
    abjad.setting(chord_1).tuplet_full_length = True
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, abjad.Chord)
    assert isinstance(chord_2, abjad.Chord)
    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2


def test_Chord___copy___04():
    """
    Chord copies tweaked note-heads.
    """

    chord_1 = abjad.Chord("<c' e' g'>4")
    abjad.tweak(chord_1.note_heads[0]).color = "red"
    chord_2 = copy.copy(chord_1)

    assert abjad.lilypond(chord_1) == abjad.String.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_2) == abjad.String.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert chord_2.note_heads[0]._client is chord_2
    assert chord_2.note_heads[1]._client is chord_2
    assert chord_2.note_heads[2]._client is chord_2

    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2

    assert chord_1.note_heads[0] == chord_2.note_heads[0]
    assert chord_1.note_heads[1] == chord_2.note_heads[1]
    assert chord_1.note_heads[2] == chord_2.note_heads[2]

    assert chord_1.note_heads[0] is not chord_2.note_heads[0]
    assert chord_1.note_heads[1] is not chord_2.note_heads[1]
    assert chord_1.note_heads[2] is not chord_2.note_heads[2]


def test_Chord___copy___05():
    """
    Chord coipes articulations and markup.
    """

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    articulation_1 = abjad.Articulation("staccato")
    abjad.attach(articulation_1, chord_1)
    markup_1 = abjad.Markup("foo", direction=abjad.Up)
    abjad.attach(markup_1, chord_1)

    chord_2 = copy.copy(chord_1)

    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2

    articulation_2 = abjad.get.indicators(chord_2, abjad.Articulation)[0]
    assert articulation_1 == articulation_2
    assert articulation_1 is not articulation_2

    markup_2 = abjad.get.markup(chord_2)[0]
    assert markup_1 == markup_2
    assert markup_1 is not markup_2
