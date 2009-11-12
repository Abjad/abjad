from abjad.tools import mathtools


def agglomerate_by_prolation(durations):
   '''Partition `durations` by implied prolation.
   
   ::

      abjad> durations = [(1, 4), (1, 8), (1, 3), (1, 6), (1, 4)]
      abjad> durtools.agglomerate_by_prolation(durations)
      [[(1, 4), (1, 8)], [(1, 3), (1, 6)], [(1, 4)]]
   '''

   assert isinstance(durations, list)
   assert 0 < len(durations)

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
