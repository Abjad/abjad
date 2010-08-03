from abjad.interfaces._Interface import _Interface


class ScoreInterface(_Interface):
   '''Report on Abjad ``Score`` in parentage of ``_client``.
   Handle no LilyPond grob.
   '''

   def __init__(self, _client):
      '''Init as type of Abjad interface.'''
      _Interface.__init__(self, _client)
   
   ## PUBLIC ATTRIBUTES ##

   @property
   def explicit(self):
      '''First explicit Abjad ``Score`` in parentage of client.
      If no explicit ``Score`` in parentage of client, return ``None``.
      '''

      from abjad.score import Score
      for parent in self._client.parentage.parentage:
         if isinstance(parent, Score):
            return parent

   @property
   def index(self):
      r'''Exact numeric location of component in score as
      a tuple of zero or more nonnegative integers. ::

         abjad> staff_1 = Staff(FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3)) * 2)
         abjad> staff_2 = Staff([FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3))])
         abjad> score = Score([staff_1, staff_2])
         abjad> pitchtools.diatonicize(score)      
         abjad> f(score)
         \new Score <<
                 \new Staff {
                         \times 2/3 {
                                 c'8
                                 d'8
                                 e'8
                         }
                         \times 2/3 {
                                 f'8
                                 g'8
                                 a'8
                         }
                 }
                 \new Staff {
                         \times 2/3 {
                                 b'8
                                 c''8
                                 d''8
                         }
                 }
         >>

      ::

         abjad> for leaf in score.leaves:
         ...     leaf, leaf.score.index
         ... 
         (Note(c', 8), (0, 0, 0))
         (Note(d', 8), (0, 0, 1))
         (Note(e', 8), (0, 0, 2))
         (Note(f', 8), (0, 1, 0))
         (Note(g', 8), (0, 1, 1))
         (Note(a', 8), (0, 1, 2))
         (Note(b', 8), (1, 0, 0))
         (Note(c'', 8), (1, 0, 1))
         (Note(d'', 8), (1, 0, 2))
      '''

      result = [ ]
      cur = self._client
      parent = cur.parentage.parent
      while parent is not None:
         index = parent.index(cur)
         result.insert(0, index)
         cur = parent
         parent = cur.parentage.parent
      result = tuple(result)
      return result
