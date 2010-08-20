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
      for spanner in list(self.attached):
         index = spanner.index(client)
         spanner._remove(client)

   def _update(self, spanners):
      '''Add list of spanners to _spanners set.'''
      self._spanners.update(spanners)

   ## PUBLIC ATTRIBUTES ##
   
   ## externalized as spannertools.get_all_spanners_attached_to_component( )
   @property
   def attached(self):
      '''Return an unordered set of all spanners 
      attaching directly to client.
      '''
      return self._spanners

   ## externalized as spannertools.get_all_spanners_attached_to_any_proper_child_of_component( )
   @property
   def children(self):
      '''Return unordered set of all spanners
      attaching to any children of self.
      Do not include spanners attaching directly to self.
      '''
#      from abjad.components._Component._Component import _Component
#      from abjad.tools import componenttools
#      result = set([ ])
#      components = componenttools.iterate_components_forward_in_expr(self._client, _Component)
#      components.next( )
#      for component in components:
#         result.update(set(component.spanners.attached))
#      return result
      from abjad.tools import spannertools
      return spannertools.get_all_spanners_attached_to_any_proper_child_of_component(
         self._client)

   ## externalized as spannertools.get_all_spanners_attached_to_any_improper_chldren_of_component( )
   @property
   def contained(self):
      '''Return unordered set of all spanners attaching to 
      components in client, including client.
      '''
#      from abjad.components._Component._Component import _Component
#      from abjad.tools import componenttools
#      result = set([ ])
#      for component in componenttools.iterate_components_forward_in_expr(self._client, _Component):
#         result.update(set(component.spanners.attached))
#      return result
      from abjad.tools import spannertools
      return spannertools.get_all_spanners_attached_to_any_improper_child_of_component(
         self._client)

   ## externalized as spannertools.is_component_with_spanner_attached( )
   @property
   def spanned(self):
      '''Return True when any spanners attach to self, 
      False otherwise.
      '''
      #return 0 < len(self.attached)
      from abjad.tools import spannertools
      return spannertools.is_component_with_spanner_attached(self._client)
