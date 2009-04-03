from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

#   ## PRIVATE ATTRIBUTES ##

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
      for spanner in self._spannersInParentage:
         result.extend(spanner._after(self._client))
      return result

   @property
   def before(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._before(self._client))
      return result

   @property
   def left(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._left(self._client))   
      return result

   @property
   def right(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._right(self._client))
      return result
