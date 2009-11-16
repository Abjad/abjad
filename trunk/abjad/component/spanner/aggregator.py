from abjad.interfaces.interface.interface import _Interface


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

   def _collectContribution(self, location):
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
      for spanner in list(self.attached):
         index = spanner.index(client)
         spanner._remove(client)

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
      from abjad.tools import iterate
      result = set([ ])
      components = iterate.naive_forward_in(self._client, _Component)
      components.next( )
      for component in components:
         result.update(set(component.spanners.attached))
      return result

   @property
   def contained(self):
      '''Return unordered set of all spanners attaching to 
         components in client, including client.'''
      from abjad.component.component import _Component
      from abjad.tools import iterate
      result = set([ ])
      for component in iterate.naive_forward_in(self._client, _Component):
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

   def report(self, output = 'screen'):
      '''Deliver report of format-time contributions.
         Order contributions first by location then by something else.'''
      result = ''
      leaf = self._client
      locations = ('before', 'left', 'right', 'after')
      spanners = list(self._spannersInParentage)
      spanners.sort(lambda x, y:
         cmp(x.__class__.__name__, y.__class__.__name__))
      for spanner in spanners:
         result += '%s\n' % spanner.__class__.__name__
         for location in locations:
            contributions = getattr(spanner.format, location)(leaf)
            if contributions:
               result += '\t%s\n' % location
               for contribution in contributions:
                  result += '\t\t%s\n' % contribution
      if output == 'screen':
         print result
      else:
         return result
