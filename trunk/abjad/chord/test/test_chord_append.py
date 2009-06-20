from abjad import *


def test_chord_append_01( ):
   r'''Append notehead sets notehead client to chord.
   A \tweak is the correct format contribution below.
   An \override an in incorrect format contribution below.'''

   chord = Chord([0, 2], Rational(1, 4))
   notehead = NoteHead(None, 11)
   notehead.style = 'harmonic'
   chord.append(notehead)

   r'''<
           c'
           d'
           \tweak #'style #'harmonic
           b'
   >4'''   

   assert check.wf(chord)
   assert notehead._client is chord
   assert chord.format == "<\n\tc'\n\td'\n\t\\tweak #'style #'harmonic\n\tb'\n>4"
