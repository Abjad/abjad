from abjad.components.Note import Note
from abjad.tools import componenttools
from abjad.tools import listtools
from abjad.tools import pitchtools


def are_stepwise_notes(*expr):
   '''.. versionadded:: 1.1.2

   True when notes in `expr` are stepwise. ::

      abjad> t = Staff(macros.scale(4))
      abjad> tonalitytools.are_stepwise_notes(t[:])
      True

   Otherwise false. ::

      abjad> tonalitytools.are_stepwise_notes(Note(0, (1, 4)), Note(0, (1, 4)))
      False

   .. versionchanged:: 1.1.2
      renamed ``tonalitytools.are_stepwise( )`` to
      ``tonalitytools.are_stepwise_notes( )``.
   '''

   for left, right in listtools.iterate_sequence_pairwise_strict(
      componenttools.iterate_components_forward_in_expr(expr, Note)):
      try:
         assert not (left.pitch == right.pitch)
         hdi = pitchtools.calculate_harmonic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(left, right)
         assert hdi.number <= 2 
      except AssertionError:
         return False

   return True
