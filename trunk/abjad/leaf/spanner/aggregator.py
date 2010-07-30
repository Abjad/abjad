from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.interfaces.interface.interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _after(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spanners_in_parentage:
         result.extend(spanner._format._after(leaf))
      return result

   ## TODO: OPTIMIZE!
   ##       Can take 16,678 function calls for a leaf in a single
   ##       staff with 100 leaves and a single spanner.
   @property
   def _before(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spanners_in_parentage:
         result.extend(spanner._format._before(leaf))
      return result

   @property
   def _left(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spanners_in_parentage:
         result.extend(spanner._format._left(leaf))   
      return result

   @property
   def _right(self):
      '''Order first by alphabetically by spanner class name;
         order next by stop / start status of spanner rel to leaf.'''
      stop_contributions = [ ]
      other_contributions = [ ]
      leaf = self.leaf
      for spanner in self._spanners_in_parentage:
         contributions = spanner._format._right(leaf)
         if contributions:
            if spanner._is_my_last_leaf(leaf):
               stop_contributions.extend(contributions)
            else:
               other_contributions.extend(contributions)
      result = stop_contributions + other_contributions
      return result

   @property
   def _spanners_in_parentage(self):
      '''List of all spanners attaching either to client
         or to a component in the parentage of client,
         ordered alphabetically by spanner class name.'''
      result = [ ]
      for component in self._client.parentage.parentage:
         result.extend(component.spanners.attached)
      result.sort(
         lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def leaf(self):
      return self._client
