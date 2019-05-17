import abjad


def test_NoteHeadList_append_01():
    """
    Append tweaked note-head to chord.
    """

    chord = abjad.Chord("<c' d'>4")
    note_head = abjad.NoteHead("b'")
    abjad.tweak(note_head).style = "harmonic"
    chord.note_heads.append(note_head)

    assert format(chord) == abjad.String.normalize(
        r"""
        <
            c'
            d'
            \tweak style #'harmonic
            b'
        >4
        """
    )

    assert note_head._client is chord
