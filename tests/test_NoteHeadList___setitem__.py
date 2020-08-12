import abjad


def test_NoteHeadList___setitem___01():
    """
    Set note-head with pitch number.
    """

    chord = abjad.Chord("<c' d'>4")
    chord.note_heads[1] = 4

    assert abjad.lilypond(chord) == "<c' e'>4"


def test_NoteHeadList___setitem___02():
    """
    Set note-head with pitch.
    """

    chord = abjad.Chord("<c' d'>4")
    chord.note_heads[1] = abjad.NamedPitch("e'")

    assert abjad.lilypond(chord) == "<c' e'>4"


def test_NoteHeadList___setitem___03():
    """
    Set note-head with tweaked note-head.
    """

    chord = abjad.Chord("<c' cs'' f''>4")
    note_head = abjad.NoteHead(3)
    abjad.tweak(note_head).color = "red"
    chord.note_heads[0] = note_head

    assert abjad.lilypond(chord) == abjad.String.normalize(
        r"""
        <
            \tweak color #red
            ef'
            cs''
            f''
        >4
        """
    )

    assert abjad.wf.wellformed(chord)
