from abjad import *
import py.test


def test_pitchtools_get_pitch_01( ):

   pitch = pitchtools.NamedPitch('df', 5)
   t = pitchtools.get_pitch(pitch)

   assert t.pair == ('df', 5)
   

def test_pitchtools_get_pitch_02( ):

   note = Note(('df', 5), (1, 4))
   t = pitchtools.get_pitch(note)

   assert t.pair == ('df', 5)
   

def test_pitchtools_get_pitch_03( ):

   note = Note(('df', 5), (1, 4))
   t = pitchtools.get_pitch(note.note_head)

   assert t.pair == ('df', 5)
   

def test_pitchtools_get_pitch_04( ):

   chord = Chord([('df', 5)], (1, 4))
   t = pitchtools.get_pitch(chord)

   assert t.pair == ('df', 5)
   

def test_pitchtools_get_pitch_05( ):

   note = Note(None, (1, 4))
   assert py.test.raises(
      MissingPitchError, 't = pitchtools.get_pitch(note)')


def test_pitchtools_get_pitch_06( ):

   note = Note(('df', 5), (1, 4))
   note.pitch = None
   assert py.test.raises(
      MissingPitchError, 't = pitchtools.get_pitch(note.note_head)')


def test_pitchtools_get_pitch_07( ):

   chord = Chord([ ], (1, 4))
   assert py.test.raises(
      MissingPitchError, 't = pitchtools.get_pitch(chord)')


def test_pitchtools_get_pitch_08( ):

   chord = Chord([0, 2, 11], (1, 4))
   assert py.test.raises(
      ExtraPitchError, 't = pitchtools.get_pitch(chord)')
