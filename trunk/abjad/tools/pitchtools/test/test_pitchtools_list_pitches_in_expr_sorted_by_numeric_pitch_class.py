from abjad import *


def test_pitchtools_list_pitches_in_expr_sorted_by_numeric_pitch_class_01( ):
   '''Works on notes.'''

   chord = Chord([-12, -10, -2, 4, 8, 11, 17, 19, 27, 30, 33, 37], (1, 4))
   sorted_pitches = pitchtools.list_pitches_in_expr_sorted_by_numeric_pitch_class(chord.pitches)

   r'''
   [pitchtools.NamedPitch(c, 3), pitchtools.NamedPitch(cs, 7), pitchtools.NamedPitch(d, 3), pitchtools.NamedPitch(ef, 6), pitchtools.NamedPitch(e, 4), pitchtools.NamedPitch(f, 5), pitchtools.NamedPitch(fs, 6), pitchtools.NamedPitch(g, 5), pitchtools.NamedPitch(af, 4), pitchtools.NamedPitch(a, 6), pitchtools.NamedPitch(bf, 3), pitchtools.NamedPitch(b, 4)]
   '''

   sorted_pitch_numbers = [pitch.number for pitch in sorted_pitches]
   sorted_pcs = [pitch.pc for pitch in sorted_pitches]

   assert sorted_pitch_numbers == [
      -12, 37, -10, 27, 4, 17, 30, 19, 8, 33, -2, 11]
   assert sorted_pcs == [
      pitchtools.NumericPitchClass(n) for n in 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
