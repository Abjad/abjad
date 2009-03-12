from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname
from abjad.helpers.iterate import iterate
from abjad.receipt.spanner import _SpannerReceipt


class _ComponentSpannerAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._spanners = set([ ])

   ## PRIVATE METHODS ##

   def _detach(self):
      '''Remove client from every spanner attaching to client.'''
      client = self._client
      receipt = _SpannerReceipt(client)
      for spanner in list(self.attached):
         index = spanner.index(client)
         receipt._pairs.add((spanner, index))
         spanner.remove(client)
      return receipt

   def _fractureContents(self):
      '''Left-fractures all spanners attaching to t and to any components
         attaching to t and starting at the same moment as t.
         Right-fractures all spanners attaching to t and to any components
         attaching to t and stopping at the same moment as t.
         Used by _Component.copy( ) only.'''
      result = [ ]
      client = self._client
      for component in client._navigator._contemporaneousStartComponents:
         for spanner in component.spanners.attached:
            result.append(spanner.fracture(spanner.index(component), 'left'))
      for component in client._navigator._contemporaneousStopComponents:
         for spanner in component.spanners.attached:
            result.append(spanner.fracture(spanner.index(component), 'right'))
      return result

   def _reattach(self, receipt):
      '''Reattach spanners described in component to client.
         Empty receipt and return client.'''
      client = self._client
      assert client is receipt._component
      for spanner, index in receipt._pairs:
         spanner.insert(index, client)
      receipt._empty( )
      return client

   def _splice(self, components):
      '''Splice components into all spanners attached self.'''
      client = self._client
      result = set([ ])
      for spanner in list(self.attached):
         index = spanner.index(client) + 1
         spanner[index:index] = components
         result.add(spanner)
      return result

   def _update(self, spanners):
      '''Added spanners to _spanners.'''
      self._spanners.update(spanners)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def attached(self):
      '''Return an unordered set of all spanners 
         attaching directly to client.'''
      return self._spanners

   @property
   def contained(self):
      '''Return an unordered set of all spanners attaching to 
         any components in client, including client.'''
      result = set([ ])
      for component in iterate(self._client, '_Component'):
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
