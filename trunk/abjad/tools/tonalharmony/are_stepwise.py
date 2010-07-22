from abjad.note import Note
from abjad.tools import iterate
from abjad.tools import listtools
from abjad.tools import pitchtools


def are_stepwise(*expr):
   '''.. versionadded:: 1.1.2

   True when notes in `expr` are stepwise. ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> tonalharmony.are_stepwise(t[:])
      True

   Otherwise false. ::

      abjad> tonalharmony.are_stepwise(Note(0, (1, 4)), Note(0, (1, 4)))
      False
   '''

   for left, right in listtools.pairwise(iterate.naive_forward_in_expr(expr, Note)):
      try:
         assert not (left.pitch == right.pitch)
         hdi = pitchtools.harmonic_diatonic_interval_from_to(left, right)
         assert hdi.number <= 2 
      except AssertionError:
         return False

   return True
