import copy

import abjad


def test_NoteHead___cmp___01():
    note_head_1 = abjad.NoteHead(12)
    note_head_2 = abjad.NoteHead(12)

    assert not note_head_1 < note_head_2
    assert note_head_1 <= note_head_2
    assert note_head_1 == note_head_2
    assert not note_head_1 != note_head_2
    assert not note_head_1 > note_head_2
    assert note_head_1 >= note_head_2


def test_NoteHead___cmp___02():
    note_head_1 = abjad.NoteHead(12)
    note_head_2 = abjad.NoteHead(13)

    assert not note_head_2 < note_head_1
    assert not note_head_2 <= note_head_1
    assert not note_head_2 == note_head_1
    assert note_head_2 != note_head_1
    assert note_head_2 > note_head_1
    assert note_head_2 >= note_head_1


def test_NoteHead___cmp___03():
    note_head_1 = abjad.NoteHead(12)
    note_head_2 = abjad.NoteHead("c''")

    assert not note_head_1 < note_head_2
    assert note_head_1 <= note_head_2
    assert note_head_1 == note_head_2
    assert not note_head_1 != note_head_2
    assert not note_head_1 > note_head_2
    assert note_head_1 >= note_head_2


def test_NoteHead___cmp___04():
    note_head_1 = abjad.NoteHead(12)
    note_head_2 = 13

    assert not note_head_2 < note_head_1
    assert not note_head_2 <= note_head_1
    assert not note_head_2 == note_head_1
    assert note_head_2 != note_head_1
    assert note_head_2 > note_head_1
    assert note_head_2 >= note_head_1


def test_NoteHead___copy___01():
    note_head_1 = abjad.NoteHead("cs''")
    note_head_1.is_cautionary = True
    note_head_1.is_forced = True
    abjad.tweak(note_head_1, r"\tweak color #red")
    abjad.tweak(note_head_1, r"\tweak font-size -2")

    note_head_2 = copy.copy(note_head_1)

    assert isinstance(note_head_1, abjad.NoteHead)
    assert isinstance(note_head_2, abjad.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
    assert note_head_1.is_cautionary == note_head_2.is_cautionary
    assert note_head_1.is_forced == note_head_2.is_forced
    assert note_head_1.tweaks == note_head_2.tweaks
    assert note_head_1.tweaks is not note_head_2.tweaks


def test_NoteHead___deepcopy___01():
    note_head_1 = abjad.NoteHead("cs''")
    abjad.tweak(note_head_1, r"\tweak color #red")
    note_head_1.is_cautionary = True
    note_head_1.is_forced = True

    note_head_2 = copy.deepcopy(note_head_1)

    assert isinstance(note_head_1, abjad.NoteHead)
    assert isinstance(note_head_2, abjad.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
    assert note_head_1.is_cautionary == note_head_2.is_cautionary
    assert note_head_1.is_forced == note_head_2.is_forced
    assert note_head_1.tweaks == note_head_2.tweaks
    assert note_head_1.tweaks is not note_head_2.tweaks


def test_NoteHead___init___01():
    """
    Initialize note-head by number.
    """

    notehead = abjad.NoteHead(6)
    assert notehead.written_pitch == abjad.NamedPitch(6)


def test_NoteHead___init___02():
    """
    Initialize note-head by LilyPond-style pitch string.
    """

    notehead = abjad.NoteHead("cs,,,")
    assert notehead.written_pitch == abjad.NamedPitch("cs,,,")


def test_NoteHead___init___03():
    """
    Initialize note-head by other note-head instance.
    """

    notehead = abjad.NoteHead(6)
    new = abjad.NoteHead(notehead)

    assert notehead is not new
    assert notehead.written_pitch == "fs'"
    assert new.written_pitch != 6


def test_NoteHead___init___04():
    """
    Initialize note-head with tweak manager.
    """

    note_head = abjad.NoteHead("cs''", tweaks=[abjad.Tweak(r"\tweak color #red")])

    assert abjad.lilypond(note_head) == "\\tweak color #red\ncs''"


def test_NoteHead_is_forced_01():
    note_head = abjad.NoteHead(written_pitch="c'")
    assert note_head.is_forced is None
    note_head.is_forced = True
    assert note_head.is_forced is True
    note_head.is_forced = False
    assert note_head.is_forced is False


def test_NoteHead_is_parenthesized_01():
    note_head = abjad.NoteHead(written_pitch="c'")
    assert note_head.is_parenthesized is None
    note_head.is_parenthesized = True
    assert note_head.is_parenthesized is True
    note_head.is_parenthesized = False
    assert note_head.is_parenthesized is False


def test_NoteHead_is_parenthesized_02():
    note_head = abjad.NoteHead(written_pitch="c'")
    note_head.is_parenthesized = True
    assert abjad.lilypond(note_head) == abjad.string.normalize(
        r"""
        \parenthesize
        c'
        """
    )


def test_NoteHead_is_parenthesized_03():
    note = abjad.Note("c'4")
    note.note_head.is_parenthesized = True
    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        \parenthesize
        c'4
        """
    )


def test_NoteHead_is_parenthesized_04():
    chord = abjad.Chord("<c' e' g'>4")
    chord.note_heads[1].is_parenthesized = True
    assert abjad.lilypond(chord) == abjad.string.normalize(
        r"""
        <
            c'
            \parenthesize
            e'
            g'
        >4
        """
    )


def test_NoteHead_written_pitch_01():
    """
    Set note-head head pitch with integer.
    """

    note = abjad.Note(13, (1, 4))
    note.note_head.written_pitch = 14

    "NoteHead(d'')"

    assert abjad.lilypond(note.note_head) == "d''"
    assert note.note_head.written_pitch != 14


def test_NoteHead_written_pitch_02():
    """
    Set note-head pitch with pitch.
    """

    note = abjad.Note(13, (1, 4))
    note.note_head.written_pitch = abjad.NamedPitch(14)

    "NoteHead(d'')"

    assert abjad.lilypond(note.note_head) == "d''"
    assert note.note_head.written_pitch != 14


def test_NoteHead_written_pitch_03():
    """
    Set note-head pitch from another note or note-head.
    Make sure this does not cause reference problems.
    """

    n1 = abjad.Note(12, (1, 4))
    n2 = abjad.Note(14, (1, 4))
    n1.written_pitch = n2.written_pitch

    assert n1.written_pitch == abjad.NamedPitch(14)
    assert n2.written_pitch == abjad.NamedPitch(14)
    assert n1.written_pitch is not n2.written_pitch
