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
      parentage = self._client._parentage._iparentage
      for component in parentage:
         result.extend(component.spanners.spanners)
      return result

   ### PRIVATE METHODS ####

   def _append(self, spanner):
      if spanner not in self._spanners:
         self._spanners.append(spanner)

   ### PUBLIC METHODS ###

#   def get(self, classname = None, grob = None, attribute = None, value = None):
#      result = self.spanners
#      if classname:
#          result = [
#            spanner for spanner in result
#            if hasname(spanner, classname)]
#      if grob:
#         result = [
#            spanner for spanner in result
#            if hasattr(spanner, '_grob') and
#            spanner._grob == grob]
#      if attribute:
#         result = [
#            spanner for spanner in result
#            if hasattr(spanner, '_attribute') and 
#            spanner._attribute == attribute]
#      if value:
#         result = [
#            spanner for spanner in result
#            if hasattr(spanner, '_value') and
#            spanner._value == value]
#      return result
