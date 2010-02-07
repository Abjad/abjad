from abjad.spanners.beam.format import _BeamSpannerFormatInterface
from abjad.tools import durtools


class _BeamComplexFormatInterface(_BeamSpannerFormatInterface):

   def __init__(self, spanner):
      _BeamSpannerFormatInterface.__init__(self, spanner)

   ## PRIVATE METHODS ##

   def _getLeftRightForExteriorLeaf(self, leaf):
      '''Get left and right flag counts for exterior leaf in spanner.'''
      spanner = self.spanner
      # lone
      if spanner._isMyOnlyLeaf(leaf):
         left, right = self._getLeftRightForLoneLeaf(leaf)
      # first
      elif spanner._isMyFirstLeaf(leaf) or not leaf.prev:
         left = 0
         #right = leaf.duration._flags
         right = durtools.rational_to_flag_count(leaf.duration.written)
      # last
      elif spanner._isMyLastLeaf(leaf) or not leaf.next:
         #left = leaf.duration._flags
         left = durtools.rational_to_flag_count(leaf.duration.written)
         right = 0
      else:
         raise ValueError('leaf must be first or last in spanner.')
      return left, right

   def _getLeftRightForInteriorLeaf(self, leaf):
      '''Interior leaves are neither first nor last in spanner.
      Interior leaves may be surrounded by beamable leaves.
      Interior leaves may be surrounded by unbeamable leaves.
      Four cases total for beamability of surrounding leaves.'''
      prev_written = leaf.prev.duration.written
      cur_written = leaf.duration.written
      next_written = leaf.next.duration.written
      prev_flag_count = durtools.rational_to_flag_count(prev_written)
      cur_flag_count = durtools.rational_to_flag_count(cur_written)
      next_flag_count = durtools.rational_to_flag_count(next_written)
      # [unbeamable leaf beamable]
      if not leaf.prev.beam.beamable and leaf.next.beam.beamable:
         #left = leaf.duration._flags
         #right = min(leaf.duration._flags, leaf.next.duration._flags)
         left = cur_flag_count
         right = min(cur_flag_count, next_flag_count)
      # [beamable leaf unbeamable]
      elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
         #left = min(leaf.duration._flags, leaf.prev.duration._flags)
         #right = leaf.duration._flags
         left = min(cur_flag_count, prev_flag_count)
         right = cur_flag_count
      # [unbeamable leaf unbeamable]
      elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
         #left = leaf.duration._flags
         #right = leaf.duration._flags
         left = cur_flag_count
         right = cur_flag_count
      # [beamable leaf beamable]
      else:
         #left = min(leaf.duration._flags, leaf.prev.duration._flags)
         #right = min(leaf.duration._flags, leaf.next.duration._flags)
         #if left != leaf.duration._flags and right != leaf.duration._flags:
         #   left = leaf.duration._flags
         left = min(cur_flag_count, prev_flag_count)
         right = min(cur_flag_count, next_flag_count)
         if left != cur_flag_count and right != cur_flag_count:
            left = cur_flag_count
      return left, right

   def _getLeftRightForLoneLeaf(self, leaf):
      '''Get left and right flag counts for only leaf in spanner.'''
      spanner = self.spanner
      left, right = None, None
      if spanner.nibs == 'left':
         #left = leaf.duration._flags
         left = cur_flag_count
         right = 0
      elif spanner.nibs == 'right':
         left = 0
         #right = leaf.duration._flags
         right = cur_flag_count
      elif spanner.nibs == 'both':
         #left = leaf.duration._flags
         #right = leaf.duration._flags
         left = cur_flag_count
         right = cur_flag_count
      elif spanner.nibs == 'neither':
         left = None
         right = None
      else:
         raise ValueError('nibs must be left, right, both or neither.')
      return left, right

   ## PUBLIC METHODS ##

   def _before(self, leaf):
      '''Spanner format contribution to output before leaf.'''
      result = [ ]
      result.extend(_BeamSpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if leaf.beam.beamable:
         if spanner._isExteriorLeaf(leaf):
            left, right = self._getLeftRightForExteriorLeaf(leaf)
         else:
            left, right = self._getLeftRightForInteriorLeaf(leaf)
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result

   def _right(self, leaf):
      '''Spanner format contribution to output right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if leaf.beam.beamable:
         # lone
         if spanner._isMyOnlyLeaf(leaf):
            if spanner.lone:
               result.append('[')
         # otherwise
         elif spanner._isMyFirstLeaf(leaf) or not leaf.prev or \
            not leaf.prev.beam.beamable:
            result.append('[')
         # lone
         if spanner._isMyOnlyLeaf(leaf):
            if spanner.lone:
               result.append(']')
         # otherwise
         elif spanner._isMyLastLeaf(leaf) or not leaf.next or \
            not leaf.next.beam.beamable:
            result.append(']')
      return result
