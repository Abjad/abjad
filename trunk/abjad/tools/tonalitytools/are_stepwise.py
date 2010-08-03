from abjad.Note import Note
from abjad.tools import iterate
from abjad.tools import listtools
from abjad.tools import pitchtools


def are_stepwise(*expr):
   '''.. versionadded:: 1.1.2

   True when notes in `expr` are stepwise. ::

      abjad> t = Staff(macros.scale(4))
      abjad> tonalitytools.are_stepwise(t[:])
      True

   Otherwise false. ::

      abjad> tonalitytools.are_stepwise(Note(0, (1, 4)), Note(0, (1, 4)))
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
