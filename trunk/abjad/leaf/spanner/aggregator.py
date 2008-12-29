from abjad.helpers.hasname import hasname
from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

   ### PRIVATE ATTRIBUTES ###

   @property
   def _after(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._after(self._client))
      return result

   @property
   def _before(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._before(self._client))
      return result

   @property
   def _left(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._left(self._client))   
      return result

   @property
   def _right(self):
      result = [ ]
      for spanner in self._spannersInParentage:
         result.extend(spanner._right(self._client))
      return result

   @property
   def _spannersInParentage(self):
      result = [ ]
      #parentage = self._client._parentage._iparentage
      for component in self._client._parentage._parentage:
         result.extend(component.spanners.attached)
      return result
