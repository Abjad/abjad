from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.factors import _factors
from abjad.rational.rational import Rational

def _agglomerate_durations_by_prolation(durations):
   '''
   Given a list of tuplet duration tokens L =  [d1, d2, d3, ..., dn], this 
   function returns a list 
   L'=[[d1, ..., dp], [dp+1, ..., dq], ..., [dq+1, ..., dn]] of sublists 
   of L, where each sublist is a group of consecutive durations with the same 
   implied prolation. 
   e.g. 
   L = [(1, 4), (1, 8), (1, 3), (1, 6), (1, 4)]
   L'= [[(1, 4), (1, 8)], [(1, 3), (1, 6)], [(1, 4)]]
   '''
   assert isinstance(durations, list)
   assert len(durations) > 0
   group = [durations[0]]
   result = [group]
   for d in durations[1:]:
      #dr = Rational(*_duration_token_unpack(d))
      #gdr =Rational(*_duration_token_unpack(group[0]))
      #dr_f = set(_factors(dr._d))
      d_f = set(_factors(d[1]))
      d_f.discard(2) 
      #gdr_f = set(_factors(gdr._d))
      gd_f = set(_factors(group[0][1]))
      gd_f.discard(2)
      if d_f == gd_f:
         group.append(d)
      else:
         group = [d]
         result.append(group)
   return result   
