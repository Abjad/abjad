from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname


class _ComponentSpannerAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._spanners = [ ]

   ### PRIVATE METHODS ###

   def _filter(self, result, classname = None, selector = None):
      if classname is not None:
         result = [p for p in result if hasname(p, classname)]
      if selector is not None:
         result = filter(selector, result)
      return result

   def _fractureContents(self):
      '''
      Left-fractures all spanners attaching to t and to any components
      attaching to t and starting at the same moment as t.
      Right-fractures all spanners attaching to t and to any components
      attaching to t and stopping at the same moment as t.

      Used by _Component.copy( ) only.
      '''
      result = [ ]
      client = self._client
      for component in client._navigator._contemporaneousStartComponents:
         for spanner in component.spanners.mine( ):
            result.append(spanner.fracture(spanner.index(component), 'left'))
      for component in client._navigator._contemporaneousStopComponents:
         for spanner in component.spanners.mine( ):
            result.append(spanner.fracture(spanner.index(component), 'right'))
      return result

   ### PUBLIC METHODS ###

   def die(self):
      for spanner in self.mine( ):
         spanner.die( )

   def fracture(self, direction = 'both'):
      result = [ ]
      client = self._client
      for spanner in self.mine( ):
         result.append(spanner.fracture(spanner.index(client), direction))
      return result

   def mine(self, classname = None, selector = None):
      result = self._spanners[ : ]
      return self._filter(result, classname, selector)
