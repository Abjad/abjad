from abjad import *


def test_pitchtools_sort_by_pc_01( ):
   '''Works on notes.'''

   chord = Chord([-12, -10, -2, 4, 8, 11, 17, 19, 27, 30, 33, 37], (1, 4))
   sorted_pitches = pitchtools.sort_by_pc(chord.pitches)

   r'''
   [Pitch(c, 3), Pitch(cs, 7), Pitch(d, 3), Pitch(ef, 6), Pitch(e, 4), Pitch(f, 5), Pitch(fs, 6), Pitch(g, 5), Pitch(af, 4), Pitch(a, 6), Pitch(bf, 3), Pitch(b, 4)]
   '''

   sorted_pitch_numbers = [pitch.number for pitch in sorted_pitches]
   sorted_pcs = [pitch.pc for pitch in sorted_pitches]

   assert sorted_pitch_numbers == [
      -12, 37, -10, 27, 4, 17, 30, 19, 8, 33, -2, 11]
   assert sorted_pcs == [
      pitchtools.PitchClass(n) for n in 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
