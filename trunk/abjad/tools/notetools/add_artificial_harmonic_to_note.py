from abjad.components.Chord import Chord
from abjad.tools import pitchtools


perfect_fourth = pitchtools.MelodicDiatonicInterval('perfect', 4)

def add_artificial_harmonic_to_note(note, melodic_diatonic_interval = perfect_fourth):
   r'''Add artifical harmonic to `note` at `melodic_diatonic_interval`::

      abjad> t = Note(0, (1, 4))
      abjad> notetools.add_artificial_harmonic_to_note(t)
      abjad> f(t)
      <
              c'
              \\tweak #'style #'harmonic
              f'
      >4

   .. versionchanged:: 1.1.2
      renamed ``harmonictools.add_artificial( )`` to
      ``notetools.add_artificial_harmonic_to_note( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.add_artificial_harmonic_to_note( )`` to
      ``notetools.add_artificial_harmonic_to_note( )``.
   '''

   chord = Chord(note)
   chord.append(chord[0].pitch.number)
   chord[1].pitch = pitchtools.tranpose_pitch_by_melodic_diatonic_interval(
      chord[1].pitch, melodic_diatonic_interval)
   chord[1].style = 'harmonic'
   return chord
