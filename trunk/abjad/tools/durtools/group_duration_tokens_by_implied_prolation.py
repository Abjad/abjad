from abjad.tools import mathtools


def group_duration_tokens_by_implied_prolation(durations):
   '''Partition `durations` by implied prolation.
   
   ::

      abjad> durations = [(1, 4), (1, 8), (1, 3), (1, 6), (1, 4)]
      abjad> durtools.group_duration_tokens_by_implied_prolation(durations)
      [[(1, 4), (1, 8)], [(1, 3), (1, 6)], [(1, 4)]]

   .. versionchanged:: 1.1.2
      renamed ``durtools.agglomerate_by_prolation( )`` to
      ``durtools.group_duration_tokens_by_implied_prolation( )``.

   .. versionchanged:: 1.1.2
      renamed ``durtools.group_durations_by_like_implied_prolation( )`` to
      ``durtools.group_duration_tokens_by_implied_prolation( )``.

   .. versionchanged:: 1.1.2
      renamed ``durtools.group_duration_tokens_by_like_implied_prolation( )`` to
      ``durtools.group_duration_tokens_by_implied_prolation( )``.
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
