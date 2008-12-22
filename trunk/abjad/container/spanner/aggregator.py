from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname


class _ContainerSpannerAggregator(_ComponentSpannerAggregator):

   ### PRIVATE METHODS ###

   def _append(self, spanner):
      if spanner not in self.spanners:
         self._spanners.append(spanner)

   ### PUBLIC METHODS ###

#   def get(self, classname = None, grob = None, attribute = None, value = None):
#      result = [ ]
#      ### TODO - use set( ) union here ###
#      for l in self._client.leaves:
#         spanners = l.spanners.get( )
#         for spanner in spanners:
#            if spanner not in result:
#               result.append(spanner)
#      if classname:
#         result = [
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
