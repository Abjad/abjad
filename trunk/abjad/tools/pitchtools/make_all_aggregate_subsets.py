from abjad.tools import mathtools
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet


def make_all_aggregate_subsets( ):
   '''.. versionadded:: 1.1.2

   Generate a list of the 4096 subsets of the twelve-tone aggregated.
   This is U* in [Morris 1987]. ::

      abjad> U_star = pitchtools.make_all_aggregate_subsets( )
      abjad> len(U_star)
      4096 
      abjad> for pcset in U_star[:20]:
         pcset
      PitchClassSet([])
      PitchClassSet([PitchClass(0)])
      PitchClassSet([PitchClass(1)])
      PitchClassSet([PitchClass(0), PitchClass(1)])
      PitchClassSet([PitchClass(2)])
      PitchClassSet([PitchClass(0), PitchClass(2)])
      PitchClassSet([PitchClass(1), PitchClass(2)])
      PitchClassSet([PitchClass(0), PitchClass(1), PitchClass(2)])
      PitchClassSet([PitchClass(3)])
      PitchClassSet([PitchClass(0), PitchClass(3)])
      PitchClassSet([PitchClass(1), PitchClass(3)])
      PitchClassSet([PitchClass(0), PitchClass(1), PitchClass(3)])
      PitchClassSet([PitchClass(2), PitchClass(3)])
      PitchClassSet([PitchClass(0), PitchClass(2), PitchClass(3)])
      PitchClassSet([PitchClass(1), PitchClass(2), PitchClass(3)])
      PitchClassSet([PitchClass(0), PitchClass(1), PitchClass(2), PitchClass(3)])
      PitchClassSet([PitchClass(4)])
      PitchClassSet([PitchClass(0), PitchClass(4)])
      PitchClassSet([PitchClass(1), PitchClass(4)])
      PitchClassSet([PitchClass(0), PitchClass(1), PitchClass(4)])
   '''

   def _helper(binary_string):
      result = zip(binary_string, range(len(binary_string)))
      result = [x[1] for x in result if x[0] == '1']
      return result

   result = [ ]

   for x in range(4096):
      subset = ''.join(list(reversed(mathtools.binary_string(x).zfill(12))))
      subset = _helper(subset)
      subset = PitchClassSet(subset)
      result.append(subset)

   return result
