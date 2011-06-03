from abjad.components import Note
from abjad.tools import componenttools
from abjad.tools import pitchtools
from abjad.tools import seqtools


def are_stepwise_ascending_notes(*expr):
   '''.. versionadded:: 1.1.2

   True when notes in `expr` are stepwise ascneding. ::

      abjad> from abjad.tools import tonalitytools

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> tonalitytools.are_stepwise_ascending_notes(t[:])
      True

   Otherwise false. ::

      abjad> tonalitytools.are_stepwise_ascending_notes(Note(0, (1, 4)), Note(0, (1, 4)))
      False

   .. versionchanged:: 1.1.2
      renamed ``tonalitytools.are_stepwise_ascending( )`` to
      ``tonalitytools.are_stepwise_ascending_notes( )``.
   '''

   for left, right in seqtools.iterate_sequence_pairwise_strict(
      componenttools.iterate_components_forward_in_expr(expr, Note)):
      try:
         assert not (left.pitch == right.pitch)
         mdi = pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(left, right)
         assert mdi.number == 2
      except AssertionError:
         return False

   return True
