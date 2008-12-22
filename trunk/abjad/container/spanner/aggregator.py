from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname


class _ContainerSpannerAggregator(_ComponentSpannerAggregator):

   ### PRIVATE METHODS ###

   def _append(self, spanner):
      if spanner not in self.spanners:
         self._spanners.append(spanner)

#   def _fractureMySpanners(self, direction = 'both'):
#      result = [ ]
#      for spanner in self.mine( ):
#         result.append(
#            spanner.fracture(spanner.index(self._client), direction))
#      return result

#   def _fractureLeafSpanners(self, direction = 'both'):
#      result = [ ]
#      if direction in ('left', 'both'):
#         for leaf in self._client._navigator._firstLeaves:
#            result.extend(leaf.spanners.fracture('left'))
#      if direction in ('right', 'both'):
#         for leaf in self._client._navigator._lastLeaves:
#            result.extend(leaf.spanners.fracture('right'))
#      return result
      
#   def _fuseLeft(self, grob = None, attribute = None, value = None):
#      result = [ ]
#      left = self._client.leaves[0]
#      spanners = left.spanners.get(grob, attribute, value)
#      for spanner in spanners[ : ]:
#         result.append(spanner.fuse(direction = 'left'))
#      return result
#
#   def _fuseRight(self, grob = None, attribute = None, value = None):
#      result = [ ]
#      right = self._client.leaves[-1]
#      spanners = right.spanners.get(grob, attribute, value)
#      for spanner in spanners[ : ]:
#         result.append(spanner.fuse(direction = 'right'))
#      return result

   ### PUBLIC METHODS ###

#   def fuse(self, grob = None, attribute = None, value = None, 
#      direction = 'both'):
#      result = [ ]
#      left, right = self._client.leaves[0], self._client.leaves[-1]
#      if direction == 'left':
#         result.extend(left.spanners.fuse(grob, attribute, value, 'left'))
#      elif direction == 'right':
#         result.extend(right.spanners.fuse(grob, attribute, value, 'right'))
#      elif direction == 'both':
#         result.extend(left.spanners.fuse(grob, attribute, value, 'left'))
#         result.extend(right.spanners.fuse(grob, attribute, value, 'right'))
#      return result

   def get(self, classname = None, grob = None, attribute = None, value = None):
      result = [ ]
      ### TODO - use set( ) union here ###
      for l in self._client.leaves:
         spanners = l.spanners.get( )
         for spanner in spanners:
            if spanner not in result:
               result.append(spanner)
      if classname:
         result = [
            spanner for spanner in result
            if hasname(spanner, classname)]
      if grob:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_grob') and
            spanner._grob == grob]
      if attribute:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_attribute') and
            spanner._attribute == attribute]
      if value:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_value') and
            spanner._value == value]
      return result
