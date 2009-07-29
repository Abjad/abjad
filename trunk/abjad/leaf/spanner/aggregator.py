from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _spannersInParentage(self):
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
   def _after(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         #result.extend(spanner.format._after(leaf))
         result.extend(spanner._format._after(leaf))
      return result

   @property
   def _before(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         #result.extend(spanner.format._before(leaf))
         result.extend(spanner._format._before(leaf))
      return result

   @property
   def leaf(self):
      return self._client

   @property
   def left(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         #result.extend(spanner.format.left(leaf))   
         result.extend(spanner._format.left(leaf))   
      return result

   @property
   def _right(self):
      '''Order first by alphabetically by spanner class name;
         order next by stop / start status of spanner rel to leaf.'''
      stop_contributions = [ ]
      other_contributions = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         #result.extend(spanner.format.right(leaf))
         #contributions = spanner.format._right(leaf)
         contributions = spanner._format._right(leaf)
         if contributions:
            if spanner._isMyLastLeaf(leaf):
               stop_contributions.extend(contributions)
            else:
               other_contributions.extend(contributions)
      result = stop_contributions + other_contributions
      return result
