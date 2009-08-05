from abjad.chord import Chord
from abjad.note import Note
from abjad.tools import iterate


def diatonicize(expr):
   '''Apply ascending diatonic pitches from zero.
      Apply to notes and chords in expr.
      Used primarily in generating test and doc file examples. 
      Compare with pitchtools.chromaticize( ).'''

   diatonic_residues = (0, 2, 4, 5, 7, 9, 11)
   length = len(diatonic_residues)

   for i, tie_chain in enumerate(iterate.tie_chains(expr)):
      pitch = int(i / length) * 12 + diatonic_residues[i % length] 
      if isinstance(tie_chain[0], Note):
         for note in tie_chain:
            note.pitch = pitch
      elif isinstance(tie_chain[0], Chord):
         for chord in tie_chain:
            chord.pitches = [pitch]
      else:
         pass
