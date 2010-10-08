from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.chordtools._split import _split


def divide_chord_by_diatonic_pitch_number(chord, pitch = NamedChromaticPitch('b', 3)):
   r'''Create two new disjunct `treble`, `bass` chords from `chord`,
   based on the diatonic pitch number of `pitch`.

   For every note head in `chord` with diatonic pitch number greater than or equal
   to the diatonic pitch number of `pitch`, add a note head to the treble chord
   returned by this function.

   For every note head in `chord` with diatonic pitch number strictly less than
   the diatonic pitch number of `pitch`, add a note head to the bass chord returned
   by this function.

   In the usual case, `chord` is an Abjad chord instance. But `chord`
   may also be an Abjad note or rest. Note that `chord` may not
   be an Abjad skip.
   

   Length treatment:

   * Zero-length parts return as Abjad rests.
   * Length-one parts return as Abjad notes.
   * Parts of length greater than ``1`` return as Abjad chords.

   Note that both the treble and bass parts returned by this function
   carry unique IDs. That is ``id(chord) != id(treble) != id(bass)``.
   
   Note also that this function returns only unspanned output.

   Example::

      abjad> chord = Chord(range(12), Fraction(1, 4))
      abjad> chord
      Chord(c' cs' d' ef' e' f' fs' g' af' a' bf' b', 4)
      abjad> chordtools.divide_chord_by_diatonic_pitch_number(chord, NamedChromaticPitch(6))
      (Chord(fs' g' af' a' bf' b', 4), Chord(c' cs' d' ef' e' f', 4))

   Preserve note head coloring. ::

      abjad> t = Chord([0, 1, 2, 3], (1, 4))
      abjad> t[0].color = 'red'
      abjad> t[1].color = 'red'
      abjad> t[2].color = 'blue'
      abjad> t[3].color = 'blue'
      abjad> f(t)
      <
              \tweak #'color #red
              c'
              \tweak #'color #red
              cs'
              \tweak #'color #blue
              d'
              \tweak #'color #blue
              ef'
      >4

   ::

      abjad> treble, bass = chordtools.divide_chord_by_diatonic_pitch_number(t, 2)     
      abjad> f(treble)
      <
              \tweak #'color #blue
              d'
              \tweak #'color #blue
              ef'
      >4

   .. versionchanged:: 1.1.2
      renamed ``chordtools.split_by_altitude( )`` to
      ``chordtools.divide_chord_by_diatonic_pitch_number( )``.

   .. versionchanged:: 1.1.2
      renamed ``chordtools.divide_chord_by_pitch_altitude( )`` to
      ``chordtools.divide_chord_by_diatonic_pitch_number( )``.
   '''

   treble, bass = _split(chord, pitch = pitch, attr = 'numbered_diatonic_pitch')

   return treble, bass
