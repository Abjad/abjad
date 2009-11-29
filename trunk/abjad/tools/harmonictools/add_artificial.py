from abjad.chord import Chord
from abjad.tools import pitchtools


perfect_fourth = pitchtools.MelodicDiatonicInterval('perfect', 4)

def add_artificial(note, diatonic_interval = perfect_fourth):
   r'''Add artifical harmonic at `diatonic_interval` to `note`.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> harmonictools.add_artificial(t)
      abjad> f(t)
      <
              c'
              \\tweak #'style #'harmonic
              f'
      >4
   '''

   chord = Chord(note)
   chord.append(chord[0].pitch.number)
   chord[1].pitch = pitchtools.transpose_by_diatonic_interval(
      chord[1].pitch, diatonic_interval)
   chord[1].style = 'harmonic'
   return chord
