# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondproxytools.LilyPondTweakReservoir \
	import LilyPondTweakReservoir


def test_NoteHead___init___01():
    r'''Init note head by number.
    '''

    notehead = notetools.NoteHead(6)
    assert notehead.written_pitch == pitchtools.NamedPitch(6)


def test_NoteHead___init___02():
    r'''Init note head by LilyPond-style pitch string.
    '''

    notehead = notetools.NoteHead('cs,,,')
    assert notehead.written_pitch == pitchtools.NamedPitch('cs,,,')


def test_NoteHead___init___03():
    r'''Init note head by other note head instance.
    '''

    notehead = notetools.NoteHead(6)
    new = notetools.NoteHead(notehead)

    assert notehead is not new
    assert notehead.written_pitch.numbered_pitch._pitch_number == 6
    assert new.written_pitch.numbered_pitch._pitch_number == 6


def test_NoteHead___init___04():
    r'''Init note head with tweak pairs.
    '''

    note_head = notetools.NoteHead("cs''", tweak_pairs=(('color', 'red'),))
    tweak = LilyPondTweakReservoir()
    tweak.color = 'red'

    assert note_head.written_pitch == pitchtools.NamedPitch("cs''")
    assert note_head.tweak == tweak
