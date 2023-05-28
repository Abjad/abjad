import abjad


def test_NoteHeadList___contains___01():
    chord = abjad.Chord("<ef' cs'' f''>4")

    assert 17 not in chord.note_heads
    assert 17.0 not in chord.note_heads
    assert abjad.NamedPitch(17) in chord.note_heads
    assert abjad.NamedPitch("f''") in chord.note_heads
    assert chord.note_heads[1] in chord.note_heads
    assert abjad.NoteHead("f''") in chord.note_heads


def test_NoteHeadList___contains___02():
    chord = abjad.Chord("<ef' cs'' f''>4")

    assert 18 not in chord.note_heads
    assert 18.0 not in chord.note_heads
    assert not abjad.NamedPitch(18) in chord.note_heads
    assert not abjad.NamedPitch("fs''") in chord.note_heads
    assert not abjad.NoteHead(18) in chord.note_heads
    assert not abjad.NoteHead("fs''") in chord.note_heads


def test_NoteHeadList___delitem___01():
    """
    Deletes note-head.
    """

    chord = abjad.Chord("<ef' cs'' f''>4")
    del chord.note_heads[1]

    assert abjad.lilypond(chord) == "<ef' f''>4"


def test_NoteHeadList___getitem___01():
    """
    Gets note-head from chord.
    """

    chord = abjad.Chord("<ef' cs'' f''>4")

    assert chord.note_heads[0] is chord.note_heads[0]
    assert chord.note_heads[1] is chord.note_heads[1]
    assert chord.note_heads[2] is chord.note_heads[2]


def test_NoteHeadList___len___01():
    assert len(abjad.Chord("<>4").note_heads) == 0
    assert len(abjad.Chord("<ef'>4").note_heads) == 1
    assert len(abjad.Chord("<ef' cs''>4").note_heads) == 2
    assert len(abjad.Chord("<ef' cs'' f''>4").note_heads) == 3


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
    abjad.tweak(note_head, r"\tweak color #red")
    chord.note_heads[0] = note_head

    assert abjad.lilypond(chord) == abjad.string.normalize(
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


def test_NoteHeadList_append_01():
    """
    Append tweaked note-head to chord.
    """

    chord = abjad.Chord("<c' d'>4")
    note_head = abjad.NoteHead("b'")
    abjad.tweak(note_head, r"\tweak style #'harmonic")
    chord.note_heads.append(note_head)

    assert abjad.lilypond(chord) == abjad.string.normalize(
        r"""
        <
            c'
            d'
            \tweak style #'harmonic
            b'
        >4
        """
    )
