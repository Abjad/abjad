from abjad import *
from abjad.core.LilyPondTweakReservoir import LilyPondTweakReservoir


def test_NoteHead___init___01():
    '''Init note head by number.
    '''

    t = notetools.NoteHead(6)
    assert t.written_pitch == pitchtools.NamedChromaticPitch(6)


def test_NoteHead___init___02():
    '''Init note head by LilyPond-style pitch string.
    '''

    t = notetools.NoteHead('cs,,,')
    assert t.written_pitch == pitchtools.NamedChromaticPitch('cs,,,')


def test_NoteHead___init___03():
    '''Init note head by other note head instance.
    '''

    t = notetools.NoteHead(6)
    new = notetools.NoteHead(t)

    assert t is not new
    assert t.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 6
    assert new.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 6


def test_NoteHead___init___04():
    '''Init note head with tweak pairs.
    '''

    note_head = notetools.NoteHead("cs''", ('color', 'red'))
    tweak = LilyPondTweakReservoir()
    tweak.color = 'red'

    assert note_head.written_pitch == pitchtools.NamedChromaticPitch("cs''")
    assert note_head.tweak == tweak
