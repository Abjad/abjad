from abjad import *


def test_pitchtools_sort_by_pc_01( ):
   '''Works on notes.'''

   chord = Chord([-12, -10, -2, 4, 8, 11, 17, 19, 27, 30, 33, 37], (1, 4))
   sorted_pitches = pitchtools.sort_by_pc(chord.pitches)

   r'''
   [NamedPitch(c, 3), NamedPitch(cs, 7), NamedPitch(d, 3), NamedPitch(ef, 6), NamedPitch(e, 4), NamedPitch(f, 5), NamedPitch(fs, 6), NamedPitch(g, 5), NamedPitch(af, 4), NamedPitch(a, 6), NamedPitch(bf, 3), NamedPitch(b, 4)]
   '''

   sorted_pitch_numbers = [pitch.number for pitch in sorted_pitches]
   sorted_pcs = [pitch.pc for pitch in sorted_pitches]

   assert sorted_pitch_numbers == [
      -12, 37, -10, 27, 4, 17, 30, 19, 8, 33, -2, 11]
   assert sorted_pcs == [
      pitchtools.PitchClass(n) for n in 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
