from abjad.chord import Chord
from abjad.tools import pitchtools


def add_artificial(note, diatonicInterval = 'perfect fourth'):
   '''>>> t = Note(0, (1, 4))
      >>> harmonictools.add_artificial(t, 'perfect fourth')
      >>> f(t)
      <
              c'
              \\tweak #'style #'harmonic
              f'
      >4'''

   chord = Chord(note)
   chord.append(chord[0].pitch.number)
   #chord[1].pitch = chord[1].pitch.diatonicTranspose(diatonicInterval)
   chord[1].pitch = pitchtools.diatonic_transpose(
      chord[1].pitch, diatonicInterval)
   chord[1].style = 'harmonic'
   return chord
