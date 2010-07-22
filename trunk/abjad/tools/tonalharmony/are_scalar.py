from abjad.note import Note
from abjad.tools import iterate
from abjad.tools import listtools
from abjad.tools import pitchtools


def are_scalar(*expr):
   '''.. versionadded:: 1.1.2

   True when notes in `expr` are scalar. ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> tonalharmony.are_scalar(t[:])
      True

   Otherwise false. ::

      abjad> tonalharmony.are_scalar(Note(0, (1, 4)), Note(0, (1, 4)))
      False
   '''

   direction_string = None
   for left, right in listtools.pairwise(iterate.naive_forward_in_expr(expr, Note)):
      try:
         assert not (left.pitch == right.pitch)
         mdi = pitchtools.melodic_diatonic_interval_from_to(left, right)
         assert mdi.number <= 2 
         if direction_string is None:
            direction_string = mdi.direction_string
         assert direction_string == mdi.direction_string
      except AssertionError:
         return False

   return True
