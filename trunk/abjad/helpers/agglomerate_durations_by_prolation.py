from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.rational.rational import Rational


def _agglomerate_durations_by_prolation(durations):
   '''Given a list of tuplet duration tokens L =  [d1, d2, d3, ..., dn], 
      this function returns a list 
      L' = [[d1, ..., dp], [dp+1, ..., dq], ..., [dq+1, ..., dn]] of sublists 
      of L, where each sublist is a group of consecutive durations 
      with the same implied prolation. 
      
      Example:

      L = [(1, 4), (1, 8), (1, 3), (1, 6), (1, 4)]
      L'= [[(1, 4), (1, 8)], [(1, 3), (1, 6)], [(1, 4)]]'''

   assert isinstance(durations, list)
   assert len(durations) > 0

   group = [durations[0]]
   result = [group]
   for d in durations[1:]:
      d_f = set(mathtools.factors(d[1]))
      d_f.discard(2) 
      gd_f = set(mathtools.factors(group[0][1]))
      gd_f.discard(2)
      if d_f == gd_f:
         group.append(d)
      else:
         group = [d]
         result.append(group)
   return result   
