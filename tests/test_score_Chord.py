import copy

import pytest

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
    abjad.override(chord_1).Staff.NoteHead.color = "#red"
    abjad.override(chord_1).Accidental.color = "#red"
    abjad.setting(chord_1).tupletFullLength = True
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
    abjad.tweak(chord_1.note_heads()[0], r"\tweak color #red")
    chord_2 = copy.copy(chord_1)

    assert abjad.lilypond(chord_1) == abjad.string.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_2) == abjad.string.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2

    assert chord_1.note_heads()[0] == chord_2.note_heads()[0]
    assert chord_1.note_heads()[1] == chord_2.note_heads()[1]
    assert chord_1.note_heads()[2] == chord_2.note_heads()[2]

    assert chord_1.note_heads()[0] is not chord_2.note_heads()[0]
    assert chord_1.note_heads()[1] is not chord_2.note_heads()[1]
    assert chord_1.note_heads()[2] is not chord_2.note_heads()[2]


def test_Chord___copy___05():
    """
    Chord copies articulations and markup.
    """

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    articulation_1 = abjad.Articulation("staccato")
    abjad.attach(articulation_1, chord_1)
    markup_1 = abjad.Markup(r"\markup foo")
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


def test_Chord___deepcopy___01():
    """
    Chord deepchopies note-heads.
    """

    chord_1 = abjad.Chord("<c' e' g'>4")
    abjad.tweak(chord_1.note_heads()[0], r"\tweak color #red")
    chord_2 = copy.deepcopy(chord_1)

    assert abjad.lilypond(chord_1) == abjad.string.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_2) == abjad.string.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2

    assert chord_1.note_heads()[0] == chord_2.note_heads()[0]
    assert chord_1.note_heads()[1] == chord_2.note_heads()[1]
    assert chord_1.note_heads()[2] == chord_2.note_heads()[2]

    assert chord_1.note_heads()[0] is not chord_2.note_heads()[0]
    assert chord_1.note_heads()[1] is not chord_2.note_heads()[1]
    assert chord_1.note_heads()[2] is not chord_2.note_heads()[2]


def test_Chord___eq____01():
    """
    Is true only when chords have the same object ID.
    """

    chord_1 = abjad.Chord("<c' e' g'>4")
    chord_2 = abjad.Chord("<c' e' g'>4")
    chord_3 = abjad.Chord("<c' e' fs'>4")

    assert chord_1 == chord_1
    assert not chord_1 == chord_2
    assert not chord_1 == chord_3
    assert not chord_2 == chord_1
    assert chord_2 == chord_2
    assert not chord_2 == chord_3
    assert not chord_3 == chord_1
    assert not chord_3 == chord_2
    assert chord_3 == chord_3


def test_Chord___init___01():
    """
    Initializes empty chord.
    """

    chord = abjad.Chord("<>4")
    assert abjad.lilypond(chord) == "<>4"


def test_Chord___init___07():
    """
    Initializes chord with LilyPond input string.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___18():
    """
    Initializes chord from LilyPond input string with forced and cautionary
    accidentals.
    """

    chord = abjad.Chord("<c!? e? g! b>4")

    assert abjad.lilypond(chord) == "<c!? e? g! b>4"


def test_Chord___init___21():
    """
    Initializes chord with drum pitches.
    """

    chord = abjad.Chord("<sn? bd! tamb>4")

    assert abjad.lilypond(chord) == "<bassdrum! snare? tambourine>4"


def test_Chord_written_pitches_01():
    """
    Returns immutable tuple of pitches in chord.
    """

    chord = abjad.Chord("<d' e' f'>4")
    pitches = chord.written_pitches()

    assert isinstance(pitches, tuple)
    assert len(pitches) == 3
    with pytest.raises(Exception):
        pitches.pop()
    with pytest.raises(Exception):
        pitches.remove(pitches[0])


def test_Chord_written_pitches_02():
    """
    Equivalent written pitches compare equal.
    """

    chord_1 = abjad.Chord("<d' e' f'>4")
    chord_2 = abjad.Chord("<d' e' f'>4")

    assert chord_1.written_pitches() == chord_2.written_pitches()


def test_Chord_set_written_pitches_01():
    """
    Sets written pitches.
    """

    chord = abjad.Chord("<>4")
    pitches = [abjad.NamedPitch(_) for _ in [4, 3, 2]]
    chord.set_written_pitches(pitches)
    assert abjad.lilypond(chord) == "<d' ef' e'>4"
