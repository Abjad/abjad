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

   ## externalized as spannertools.get_all_spanners_attached_to_any_proper_children_of_component( )
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
      return spannertools.get_all_spanners_attached_to_any_proper_children_of_component(
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
      return spannertools.get_all_spanners_attached_to_any_improper_children_of_component(
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

   ## PUBLIC METHODS ##

   ## externalized as spannertools.destroy_all_spanners_attached_to_component( )
   def clear(self):
      '''Clear every spanner attaching to client.
      '''
      #for spanner in list(self.attached):
      #   spanner.clear( )
      from abjad.tools import spannertools
      spannertools.destroy_all_spanners_attached_to_component(self._client)

   ## externalized as spannertools.fracture_all_spananers_attached_to_component( )
   def fracture(self, direction = 'both'):
      '''Fracture every spanner attaching to client.
      '''
#      result = [ ]
#      client = self._client
#      for spanner in self.attached:
#         result.append(spanner.fracture(spanner.index(client), direction))
#      return result
      from abjad.tools import spannertools
      return spannertools.fracture_all_spanners_attached_to_component(self._client, direction)

   ## externalized as spannertools.get_all_spanners_attached_to_component( )
   def get_all_attached_spanners_of_type(self, spanner_type):
      #return set([x for x in self.attached if isinstance(x, spanner_type)])
      from abjad.tools import spannertools
      return spannertools.get_all_spanners_attached_to_component(self._client, spanner_type)

   ## externalized as spannertools.report_as_string_format_contributions_of_spanners_attached_to_component( )
   ## externalized as spannertools.report_as_string_format_contributions_of_spanners_attached_to_improper_parentage_of_component( )
   ## externalized as spannertools.report_to_screen_format_contributions_of_spanners_attached_to_component( )
   ## externalized as spannertools.report_to_screen_format_contributions_of_spanners_attached_to_improper_parentage_of_component( )
   def report(self, output = 'screen'):
      '''Deliver report of format-time contributions.
      Order contributions first by location then by something else.
      '''
#      result = ''
#      leaf = self._client
#      locations = ('before', 'left', 'right', 'after')
#      spanners = list(self._spanners_in_parentage)
#      spanners.sort(lambda x, y:
#         cmp(x.__class__.__name__, y.__class__.__name__))
#      for spanner in spanners:
#         result += '%s\n' % spanner.__class__.__name__
#         for location in locations:
#            contributions = getattr(spanner.format, location)(leaf)
#            if contributions:
#               result += '\t%s\n' % location
#               for contribution in contributions:
#                  result += '\t\t%s\n' % contribution
#      if output == 'screen':
#         print result
#      else:
#         return result
      from abjad.tools import spannertools
      spannertools.report_as_string_format_contributions_of_all_spanners_attached_to_component(
         self._client)
