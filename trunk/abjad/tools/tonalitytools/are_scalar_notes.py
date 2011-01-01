from abjad.components import Note
from abjad.tools import componenttools
from abjad.tools import seqtools
from abjad.tools import pitchtools


def are_scalar_notes(*expr):
   '''.. versionadded:: 1.1.2

   True when notes in `expr` are scalar. ::

      abjad> t = Staff(macros.scale(4))
      abjad> tonalitytools.are_scalar_notes(t[:])
      True

   Otherwise false. ::

      abjad> tonalitytools.are_scalar_notes(Note(0, (1, 4)), Note(0, (1, 4)))
      False

   .. versionchanged:: 1.1.2
      renamed ``tonalitytools.are_scalar( )`` to
      ``tonalitytools.are_scalar_notes( )``.
   '''

   direction_string = None
   for left, right in seqtools.iterate_sequence_pairwise_strict(
      componenttools.iterate_components_forward_in_expr(expr, Note)):
      try:
         assert not (left.pitch == right.pitch)
         mdi = pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(left, right)
         assert mdi.number <= 2 
         if direction_string is None:
            direction_string = mdi.direction_string
         assert direction_string == mdi.direction_string
      except AssertionError:
         return False

   return True
