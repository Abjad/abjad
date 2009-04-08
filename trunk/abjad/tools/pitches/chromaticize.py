from abjad.chord.chord import Chord
from abjad.helpers.iterate_tie_chains import iterate_tie_chains
from abjad.note.note import Note


def chromaticize(expr):
   '''Apply ascending chromatic pitches from zero 
      to the notes and chords in expr.
      Used primarily in generating test and doc file examples. 
      Compare with pitches.diatonicize( ).'''

   for i, x in enumerate(iterate_tie_chains(expr)):
      pitch = i
      if isinstance(x[0], Note):
         for note in x:
            note.pitch = pitch
      elif isinstance(x[0], Chord):
         for chord in x:
            chord.pitches = [pitch]
      else:
         pass
