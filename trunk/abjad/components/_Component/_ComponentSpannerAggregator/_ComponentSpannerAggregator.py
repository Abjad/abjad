from abjad.interfaces._Interface import _Interface


class _ComponentSpannerAggregator(_Interface):
   '''Aggregate information about all spanners affecting client.'''

   def __init__(self, client):
      '''Bind to client and set spanners to empty set.'''
      _Interface.__init__(self, client)
      self._spanners = set([ ])

   ## PRIVATE METHODS ##

   def _add(self, spanner):
      '''Add spanner to _spanners set.'''
      self._spanners.add(spanner)

   def _collect_contribution(self, location):
      '''Return unordered set of format-time contributions for location.'''
      result = set([ ])
      assert isinstance(location, str)
      assert not location.startswith('_')
      without_underscore = getattr(self, location, None)
      if without_underscore is not None:
         result.update(without_underscore)
      with_underscore = getattr(self, '_' + location, None)
      if with_underscore:
         result.update(with_underscore)
      return result

   def _detach(self):
      '''Remove client from every spanner attaching to client.'''
      client = self._client
      #for spanner in list(self.attached):
      for spanner in list(self._spanners):
         index = spanner.index(client)
         spanner._remove(client)

   def _update(self, spanners):
      '''Add list of spanners to _spanners set.'''
      self._spanners.update(spanners)
