from abjad.tools import mathtools
from abjad.tools.pitchtools.NumericPitchClassSet import NumericPitchClassSet


def make_all_aggregate_subsets( ):
   '''.. versionadded:: 1.1.2

   List all 4096 subsets of the twelve-tone aggregate. ::

      abjad> U_star = pitchtools.make_all_aggregate_subsets( )
      abjad> len(U_star)
      4096 
      abjad> for pcset in U_star[:20]:
         pcset
      NumericPitchClassSet([])
      NumericPitchClassSet([PitchClass(0)])
      NumericPitchClassSet([PitchClass(1)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(1)])
      NumericPitchClassSet([PitchClass(2)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(2)])
      NumericPitchClassSet([PitchClass(1), NumericPitchClass(2)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(1), NumericPitchClass(2)])
      NumericPitchClassSet([PitchClass(3)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(1), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(1), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(2), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(2), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(1), NumericPitchClass(2), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(1), NumericPitchClass(2), NumericPitchClass(3)])
      NumericPitchClassSet([PitchClass(4)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(4)])
      NumericPitchClassSet([PitchClass(1), NumericPitchClass(4)])
      NumericPitchClassSet([PitchClass(0), NumericPitchClass(1), NumericPitchClass(4)])

   This is ``U*`` in [Morris 1987].
   '''

   def _helper(binary_string):
      result = zip(binary_string, range(len(binary_string)))
      result = [x[1] for x in result if x[0] == '1']
      return result

   result = [ ]

   for x in range(4096):
      subset = ''.join(list(reversed(mathtools.integer_to_binary_string(x).zfill(12))))
      subset = _helper(subset)
      subset = NumericPitchClassSet(subset)
      result.append(subset)

   return result
