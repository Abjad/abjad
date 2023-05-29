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
    abjad.tweak(chord_1.note_heads[0], r"\tweak color #red")
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
    abjad.tweak(chord_1.note_heads[0], r"\tweak color #red")
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

    assert chord_1.note_heads[0] == chord_2.note_heads[0]
    assert chord_1.note_heads[1] == chord_2.note_heads[1]
    assert chord_1.note_heads[2] == chord_2.note_heads[2]

    assert chord_1.note_heads[0] is not chord_2.note_heads[0]
    assert chord_1.note_heads[1] is not chord_2.note_heads[1]
    assert chord_1.note_heads[2] is not chord_2.note_heads[2]


def test_Chord___eq____01():
    """
    True only when chords have the same object ID.
    """

    chord_1 = abjad.Chord([0, 4, 7], (1, 4))
    chord_2 = abjad.Chord([0, 4, 7], (1, 4))
    chord_3 = abjad.Chord([0, 4, 6], (1, 4))

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
    Initialize empty chord.
    """

    chord = abjad.Chord([], (1, 4))
    assert abjad.lilypond(chord) == "<>4"


def test_Chord___init___02():
    """
    Initialize chord with pitch numbers.
    """

    chord = abjad.Chord([2, 4, 5], (1, 4))
    assert abjad.lilypond(chord) == "<d' e' f'>4"


def test_Chord___init___03():
    """
    Initialize chord with pitch tokens.
    """

    chord = abjad.Chord([("ds", 4), ("ef", 4)], (1, 4))
    assert abjad.lilypond(chord) == "<ds' ef'>4"


def test_Chord___init___04():
    """
    Initialize chord with pitches.
    """

    pitches = []
    pitches.append(abjad.NamedPitch("D#4"))
    pitches.append(abjad.NamedPitch("Eb4"))
    chord = abjad.Chord(pitches, (1, 4))
    assert abjad.lilypond(chord) == "<ds' ef'>4"


def test_Chord___init___05():
    """
    Initialize chord with pitches and pitch numbers together.
    """

    pitches = [2, ("ef", 4), abjad.NamedPitch(4)]
    chord = abjad.Chord(pitches, (1, 4))
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___06():
    """
    Initialize chord with list of pitch names.
    """

    pitches = ["d'", "ef'", "e'"]
    chord = abjad.Chord(pitches, (1, 4))
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___07():
    """
    Initialize chord with LilyPond input string.
    """

    chord = abjad.Chord("<d' ef' e'>4")
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord___init___08():
    """
    Initialize chord from skip.
    """

    skip = abjad.Skip("s8")
    chord = abjad.Chord(skip)

    assert abjad.lilypond(skip) == "s8"
    assert abjad.lilypond(chord) == "<>8"

    assert abjad.wf.wellformed(skip)
    assert abjad.wf.wellformed(chord)


def test_Chord___init___09():
    """
    Initialize chord from tupletized skip.
    """

    tuplet = abjad.Tuplet((2, 3), "s8 s8 s8")
    chord = abjad.Chord(tuplet[0])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.get.parentage(chord).parent is None
    assert abjad.wf.wellformed(chord)


def test_Chord___init___10():
    """
    Initialize chord from containerized skip.
    """

    tuplet = abjad.Voice("s8 s8 s8")
    chord = abjad.Chord(tuplet[0])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.get.parentage(chord).parent is None
    assert abjad.wf.wellformed(chord)


def test_Chord___init___11():
    """
    Initialize chord from beamed skip.
    """

    staff = abjad.Staff("c'8 [ s8 c'8 ]")
    chord = abjad.Chord(staff[1])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.get.parentage(chord).parent is None
    assert abjad.wf.wellformed(chord)


def test_Chord___init___12():
    """
    Initialize chord from rest.
    """

    rest = abjad.Rest("r8")
    chord = abjad.Chord(rest)

    assert abjad.lilypond(rest) == "r8"
    assert abjad.lilypond(chord) == "<>8"
    assert abjad.wf.wellformed(rest)
    assert abjad.wf.wellformed(chord)


def test_Chord___init___13():
    """
    Initialize chord from tupletized rest.
    """

    tuplet = abjad.Tuplet((2, 3), "r8 r8 r8")
    chord = abjad.Chord(tuplet[1])

    assert abjad.lilypond(chord) == "<>8"
    assert abjad.wf.wellformed(chord)
    assert abjad.get.parentage(chord).parent is None


def test_Chord___init___14():
    """
    Initialize chord from note.
    """

    note = abjad.Note("d'8")
    chord = abjad.Chord(note)

    assert abjad.lilypond(note) == "d'8"
    assert abjad.lilypond(chord) == "<d'>8"
    assert abjad.wf.wellformed(note)
    assert abjad.wf.wellformed(chord)


def test_Chord___init___15():
    """
    Initialize chord from tupletized note.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    chord = abjad.Chord(tuplet[1])

    assert abjad.lilypond(chord) == "<c'>8"
    assert abjad.wf.wellformed(chord)
    assert abjad.get.parentage(chord).parent is None


def test_Chord___init___16():
    """
    Initialize chord from spanned note.
    """

    staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
    chord = abjad.Chord(staff[1])

    assert abjad.lilypond(chord) == "<d'>8"
    assert abjad.wf.wellformed(chord)
    assert abjad.get.parentage(chord).parent is None


def test_Chord___init___17():
    """
    Initialize empty chord from LilyPond input string.
    """

    chord = abjad.Chord("<>8.")

    assert abjad.lilypond(chord) == "<>8."
    assert not len(chord.note_heads)


def test_Chord___init___18():
    """
    Initialize chord from LilyPond input string with forced and cautionary
    accidentals.
    """

    chord = abjad.Chord("<c!? e? g! b>4")

    assert abjad.lilypond(chord) == "<c!? e? g! b>4"


def test_Chord___init___19():
    """
    Initialize chord from note with forced and cautionary accidentals.
    """

    note = abjad.Note("c'!?4")
    chord = abjad.Chord(note)

    assert abjad.lilypond(chord) == "<c'!?>4"


def test_Chord___init___20():
    """
    Initialize chord from other chord.
    """

    chord_1 = abjad.Chord("<c' e' g' bf'>4")
    chord_2 = abjad.Chord(chord_1, abjad.Duration(1, 8))

    assert abjad.lilypond(chord_2) == "<c' e' g' bf'>8"


def test_Chord___init___21():
    """
    Initialize chord with drum pitches.
    """

    chord = abjad.Chord("<sn? bd! tamb>4")

    assert abjad.lilypond(chord) == "<bassdrum! snare? tambourine>4"


def test_Chord_written_pitches_01():
    """
    Returns immutable tuple of pitches in chord.
    """

    chord = abjad.Chord("<d' e' f'>4")
    pitches = chord.written_pitches

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

    assert chord_1.written_pitches == chord_2.written_pitches


def test_Chord_written_pitches_03():
    """
    Set written pitches with pitch numbers.
    """

    chord = abjad.Chord([], (1, 4))
    chord.written_pitches = [4, 3, 2]
    assert abjad.lilypond(chord) == "<d' ef' e'>4"

    chord.written_pitches = (4, 3, 2)
    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord_written_pitches_04():
    """
    Set written pitches with pitches.
    """

    chord = abjad.Chord([], (1, 4))
    chord.written_pitches = [
        abjad.NamedPitch(4),
        abjad.NamedPitch(3),
        abjad.NamedPitch(2),
    ]

    assert abjad.lilypond(chord) == "<d' ef' e'>4"


def test_Chord_written_pitches_05():
    """
    Set written pitches with both pitches and pitch numbers.
    """

    chord = abjad.Chord([], (1, 4))
    chord.written_pitches = [4, abjad.NamedPitch(3), abjad.NamedPitch(2)]

    assert abjad.lilypond(chord) == "<d' ef' e'>4"
