from abjad import *
import py.test


def test_NoteHead_written_pitch_01():
    '''Set Note head pitch with integer.
    '''

    t = Note(13, (1, 4))
    t.note_head.written_pitch = 14

    "NoteHead(d'')"

    assert t.note_head.format == "d''"
    assert t.note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 14


def test_NoteHead_written_pitch_02():
    '''Set Note head pitch with pitch.
    '''

    t = Note(13, (1, 4))
    t.note_head.written_pitch = pitchtools.NamedChromaticPitch(14)

    "NoteHead(d'')"

    assert t.note_head.format == "d''"
    assert t.note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 14


def test_NoteHead_written_pitch_03():
    '''Can not set note head pitch to none.
    '''

    t = Note(13, (1, 4))

    assert py.test.raises(Exception, 't.note_head.written_pitch = None')


def test_NoteHead_written_pitch_04():
    '''Set note head pitch from another note or note head.
    Make sure this does not cause reference problems.
    '''

    n1 = Note(12, (1, 4))
    n2 = Note(14, (1, 4))
    n1.written_pitch = n2.written_pitch

    assert n1.written_pitch == pitchtools.NamedChromaticPitch(14)
    assert n2.written_pitch == pitchtools.NamedChromaticPitch(14)
    assert n1.written_pitch is not n2.written_pitch
