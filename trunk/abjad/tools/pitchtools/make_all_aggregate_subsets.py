from abjad.tools import mathtools
from PCSet import PCSet


def make_all_aggregate_subsets( ):
   '''.. versionadded:: 1.1.2

   Generate a list of the 4096 subsets of the twelve-tone aggregated.
   This is U* in [Morris 1987]. ::

      abjad> U_star = pitchtools.make_all_aggregate_subsets( )
      abjad> len(U_star)
      4096 
      abjad> for pcset in U_star[:20]:
         pcset
      PCSet([])
      PCSet([PC(0)])
      PCSet([PC(1)])
      PCSet([PC(0), PC(1)])
      PCSet([PC(2)])
      PCSet([PC(0), PC(2)])
      PCSet([PC(1), PC(2)])
      PCSet([PC(0), PC(1), PC(2)])
      PCSet([PC(3)])
      PCSet([PC(0), PC(3)])
      PCSet([PC(1), PC(3)])
      PCSet([PC(0), PC(1), PC(3)])
      PCSet([PC(2), PC(3)])
      PCSet([PC(0), PC(2), PC(3)])
      PCSet([PC(1), PC(2), PC(3)])
      PCSet([PC(0), PC(1), PC(2), PC(3)])
      PCSet([PC(4)])
      PCSet([PC(0), PC(4)])
      PCSet([PC(1), PC(4)])
      PCSet([PC(0), PC(1), PC(4)])
   '''

   def _helper(binary_string):
      result = zip(binary_string, range(len(binary_string)))
      result = [x[1] for x in result if x[0] == '1']
      return result

   result = [ ]

   for x in range(4096):
      subset = ''.join(list(reversed(mathtools.binary_string(x).zfill(12))))
      subset = _helper(subset)
      subset = PCSet(subset)
      result.append(subset)

   return result
