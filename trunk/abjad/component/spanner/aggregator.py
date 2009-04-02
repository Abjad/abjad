from abjad.core.interface import _Interface
from abjad.helpers.iterate import iterate
from abjad.receipt.spanner import _SpannerReceipt


class _ComponentSpannerAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._spanners = set([ ])

   ## PRIVATE METHODS ##

   def _add(self, spanner):
      '''Add spanner to _spanners set.'''
      self._spanners.add(spanner)

   def _detach(self):
      '''Remove client from every spanner attaching to client.'''
      client = self._client
      receipt = _SpannerReceipt(client)
      for spanner in list(self.attached):
         index = spanner.index(client)
         receipt._pairs.add((spanner, index))
         spanner._remove(client)
      return receipt

   def _reattach(self, receipt):
      '''Reattach spanners described in component to client.
         Empty receipt and return client.'''
      client = self._client
      assert client is receipt._component
      for spanner, index in receipt._pairs:
         spanner._insert(index, client)
      receipt._empty( )
      return client

   def _update(self, spanners):
      '''Add list of spanners to _spanners set.'''
      self._spanners.update(spanners)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def attached(self):
      '''Return an unordered set of all spanners 
         attaching directly to client.'''
      return self._spanners

   @property
   def children(self):
      '''Return unordered set of all spanners
         attaching to any children of self.
         Do not include spanners attaching directly to self.'''
      from abjad.component.component import _Component
      result = set([ ])
      components = iterate(self._client, _Component)
      components.next( )
      for component in components:
         result.update(set(component.spanners.attached))
      return result

   @property
   def contained(self):
      '''Return unordered set of all spanners attaching to 
         components in client, including client.'''
      from abjad.component.component import _Component
      result = set([ ])
      for component in iterate(self._client, _Component):
         result.update(set(component.spanners.attached))
      return result

   @property
   def spanned(self):
      '''Return True when any spanners attach to self, 
         False otherwise.'''
      return len(self.attached) > 0

   ## PUBLIC METHODS ##

   def clear(self):
      '''Clear every spanner attaching to client.'''
      for spanner in list(self.attached):
         spanner.clear( )

   def fracture(self, direction = 'both'):
      '''Fracture every spanner attaching to client.'''
      result = [ ]
      client = self._client
      for spanner in self.attached:
         result.append(spanner.fracture(spanner.index(client), direction))
      return result
