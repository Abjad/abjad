from abjad.tools import mathtools
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet


def inventory_aggregate_subsets( ):
   '''.. versionadded:: 1.1.2

   Inventory aggregate subsets::

      abjad> U_star = pitchtools.inventory_aggregate_subsets( )
      abjad> len(U_star)
      4096 
      abjad> for pcset in U_star[:20]:
         pcset
      NumberedChromaticPitchClassSet([ ])
      NumberedChromaticPitchClassSet([PitchClass(0)])
      NumberedChromaticPitchClassSet([PitchClass(1)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(1)])
      NumberedChromaticPitchClassSet([PitchClass(2)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(2)])
      NumberedChromaticPitchClassSet([PitchClass(1), NumberedChromaticPitchClass(2)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(1), NumberedChromaticPitchClass(2)])
      NumberedChromaticPitchClassSet([PitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(1), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(1), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(2), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(2), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(1), NumberedChromaticPitchClass(2), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(1), NumberedChromaticPitchClass(2), NumberedChromaticPitchClass(3)])
      NumberedChromaticPitchClassSet([PitchClass(4)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(4)])
      NumberedChromaticPitchClassSet([PitchClass(1), NumberedChromaticPitchClass(4)])
      NumberedChromaticPitchClassSet([PitchClass(0), NumberedChromaticPitchClass(1), NumberedChromaticPitchClass(4)])

   There are 4096 subsets of the aggregate.

   This is ``U*`` in [Morris 1987].

   Return list of numbered chromatic pitch-class sets.
   '''

   def _helper(binary_string):
      result = zip(binary_string, range(len(binary_string)))
      result = [x[1] for x in result if x[0] == '1']
      return result

   result = [ ]

   for x in range(4096):
      subset = ''.join(list(reversed(mathtools.integer_to_binary_string(x).zfill(12))))
      subset = _helper(subset)
      subset = NumberedChromaticPitchClassSet(subset)
      result.append(subset)

   return result
