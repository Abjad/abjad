def apply_accidental_to_named_pitch(named_pitch, accidental = None):
   '''Apply `accidental` to `named_pitch`.

   Return new named pitch.
   '''

   from abjad.tools.pitchtools.Accidental import Accidental
   accidental = Accidental(accidental)
   new_accidental = named_pitch.accidental + accidental
   new_name = named_pitch.letter + new_accidental.alphabetic_string
   return type(named_pitch)(new_name, named_pitch.octave)
