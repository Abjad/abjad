from abjad.core.interface import _Interface


class _ScoreInterface(_Interface):
   '''Report on *Abjad* ``Score`` in parentage of ``_client``.
      Handle no *LilyPond* grob.'''

   def __init__(self, _client):
      '''Init as type of *Abjad* interface.'''
      _Interface.__init__(self, _client)
   
   ## PUBLIC ATTRIBUTES ##

   @property
   def explicit(self):
      '''First explicit *Abjad* ``Score`` in parentage of client.
         If no explicit ``Score`` in parentage of client, return ``None``.'''
      from abjad.score import Score
      for parent in self._client.parentage.parentage:
         if isinstance(parent, Score):
            return parent
