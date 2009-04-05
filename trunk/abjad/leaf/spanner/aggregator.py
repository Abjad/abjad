from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _spannersInParentage(self):
      result = [ ]
      for component in self._client.parentage.parentage:
         result.extend(component.spanners.attached)
      result.sort(
         lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         result.extend(spanner.format.after(leaf))
      return result

   @property
   def before(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         result.extend(spanner.format.before(leaf))
      return result

   @property
   def leaf(self):
      return self._client

   @property
   def left(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         result.extend(spanner.format.left(leaf))   
      return result

   @property
   def right(self):
      result = [ ]
      leaf = self.leaf
      for spanner in self._spannersInParentage:
         result.extend(spanner.format.right(leaf))
      return result
