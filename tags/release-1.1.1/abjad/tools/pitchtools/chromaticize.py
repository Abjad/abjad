from abjad.chord import Chord
from abjad.note import Note
from abjad.tools import iterate


def chromaticize(expr):
   '''Apply ascending chromatic pitches from zero 
      to the notes and chords in expr.
      Used primarily in generating test and doc file examples. 
      Compare with pitchtools.diatonicize( ).'''

   for i, x in enumerate(iterate.tie_chains(expr)):
      pitch = i
      if isinstance(x[0], Note):
         for note in x:
            note.pitch = pitch
      elif isinstance(x[0], Chord):
         for chord in x:
            chord.pitches = [pitch]
      else:
         pass
