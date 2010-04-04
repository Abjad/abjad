from abjad.note import Note
from abjad.tools import listtools
from abjad.tools import pitchtools


def are_scalar(*notes):
   '''.. versionadded:: 1.1.2

   True when `notes` are scalar. ::

      abjad> t = Staff(construct.scale(4))
      abjad> tonalharmony.are_scalar(t[:])
      True

   Otherwise false. ::

      abjad> tonalharmony.are_scalar(Note(0, (1, 4)), Note(0, (1, 4)))
      False
   '''

   for left, right in listtools.pairwise(notes):
      try:
         assert not (left.pitch == right.pitch)
         hdi = pitchtools.harmonic_diatonic_interval_from_to(left, right)
         assert hdi.number <= 2 
      except AssertionError:
         return False

   return True
