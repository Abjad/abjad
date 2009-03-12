from abjad.helpers.iterate import iterate


## TODO - write tests

def appictate(expr):
   '''Apply ascending chromatic pitches from zero 
      to the notes and chords in expr.
      Used primarily in generating test and doc file examples. 
      Coined term.'''

   from abjad.chord.chord import Chord
   from abjad.leaf.leaf import _Leaf
   from abjad.note.note import Note

   for i, x in enumerate(iterate(expr, _Leaf)):
      if isinstance(x, Note):
         x.pitch = i
      elif isinstance(x, Chord):
         x.pitches = [i] 
      else:
         pass
