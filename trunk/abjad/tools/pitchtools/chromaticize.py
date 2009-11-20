from abjad.chord import Chord
from abjad.note import Note
from abjad.tools import iterate


def chromaticize(expr):
   r'''Apply ascending chromatic pitches 
   to the notes and chords in `expr`. ::

      abjad> staff = Voice(construct.notes(0, [(5, 32)] * 4))
      abjad> pitchtools.chromaticize(staff)
      abjad> f(staff)
      \new Voice {
              c'8 ~
              c'32
              cs'8 ~
              cs'32
              d'8 ~
              d'32
              ef'8 ~
              ef'32
      }

   Used primarily in generating test file examples.
   '''

   for i, x in enumerate(iterate.tie_chains_forward_in(expr)):
      pitch = i
      if isinstance(x[0], Note):
         for note in x:
            note.pitch = pitch
      elif isinstance(x[0], Chord):
         for chord in x:
            chord.pitches = [pitch]
      else:
         pass
