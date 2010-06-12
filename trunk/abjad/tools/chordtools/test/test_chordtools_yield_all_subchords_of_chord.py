from abjad import *


def test_chordtools_yield_all_subchords_of_chord_01( ):

   chord = Chord([0, 2, 8, 9], (1, 4))
   generator = chordtools.yield_all_subchords_of_chord(chord)
   subchords = list(generator)
   pairs = [subchord.pairs for subchord in subchords]

   assert pairs == [
      (),
      (('c', 4),),
      (('d', 4),),
      (('c', 4), ('d', 4)),
      (('af', 4),),
      (('c', 4), ('af', 4)),
      (('d', 4), ('af', 4)),
      (('c', 4), ('d', 4), ('af', 4)),
      (('a', 4),),
      (('c', 4), ('a', 4)),
      (('d', 4), ('a', 4)),
      (('c', 4), ('d', 4), ('a', 4)),
      (('af', 4), ('a', 4)),
      (('c', 4), ('af', 4), ('a', 4)),
      (('d', 4), ('af', 4), ('a', 4)),
      (('c', 4), ('d', 4), ('af', 4), ('a', 4))]
