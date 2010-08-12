from abjad.components.Chord import Chord
from abjad.components.Note import Note


def set_ascending_chromatic_pitches_on_nontied_pitched_components_in_expr(expr):
   r'''Apply ascending chromatic pitches 
   to the notes and chords in `expr`. ::

      abjad> staff = Voice(notetools.make_notes(0, [(5, 32)] * 4))
      abjad> macros.chromaticize(staff)
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

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.chromaticize( )`` to
      ``macros.chromaticize( )``.
   '''
   from abjad.tools import tietools 

   for i, x in enumerate(tietools.iterate_tie_chains_forward_in_expr(expr)):
      pitch = i
      if isinstance(x[0], Note):
         for note in x:
            note.pitch = pitch
      elif isinstance(x[0], Chord):
         for chord in x:
            chord.pitches = [pitch]
      else:
         pass
