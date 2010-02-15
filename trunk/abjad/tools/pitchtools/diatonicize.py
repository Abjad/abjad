from abjad.chord import Chord
from abjad.note import Note
from abjad.pitch import Pitch
from abjad.tools import iterate


def diatonicize(expr):
   r'''Apply ascending diatonic pitches to the notes
   and chords in `expr`. ::

      abjad> staff = Staff(construct.notes(0, [(5, 32)] * 4))
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'32
         d'8 ~
         d'32
         e'8 ~
         e'32
         f'8 ~
         f'32
      }

   Used primarily in generating test file examples.
   '''
   from abjad.tools import tonalharmony

   scale = tonalharmony.Scale('d', 'major')

   diatonic_residues = (0, 2, 4, 5, 7, 9, 11)
   length = len(diatonic_residues)
   #length = len(scale)

   octave_number = 4
   start_pitch = Pitch(scale[0], octave_number)
   for i, tie_chain in enumerate(iterate.tie_chains_forward_in(expr)):
      pitch = int(i / length) * 12 + diatonic_residues[i % length] 
      #named_pitch_class = scale[i % length]
      #pitch_class_number = named_pitch_class.pitch_class.number
      #pitch_number = int(i / length) * 12 + pitch_class_number
      #pitch = Pitch(pitch_number, named_pitch_class)
      if isinstance(tie_chain[0], Note):
         for note in tie_chain:
            note.pitch = pitch
      elif isinstance(tie_chain[0], Chord):
         for chord in tie_chain:
            chord.pitches = [pitch]
      else:
         pass
