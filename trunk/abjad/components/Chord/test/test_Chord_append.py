from abjad import *


def test_Chord_append_01( ):
   r'''Append note_head sets note_head client to chord.
   A \tweak is the correct format contribution below.
   An \override an in incorrect format contribution below.
   '''

   chord = Chord([0, 2], Rational(1, 4))
   note_head = NoteHead(None, 11)
   note_head.tweak.style = 'harmonic'
   chord.append(note_head)

   r'''
   <
           c'
           d'
           \tweak #'style #'harmonic
           b'
   >4
   '''

   assert componenttools.is_well_formed_component(chord)
   assert note_head._client is chord
   assert chord.format == "<\n\tc'\n\td'\n\t\\tweak #'style #'harmonic\n\tb'\n>4"
