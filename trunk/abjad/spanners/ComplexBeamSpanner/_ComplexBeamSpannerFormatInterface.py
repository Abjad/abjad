from abjad.spanners.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface
from abjad.tools import durtools


class _ComplexBeamSpannerFormatInterface(_BeamSpannerFormatInterface):

   def __init__(self, spanner):
      _BeamSpannerFormatInterface.__init__(self, spanner)

   ## PRIVATE METHODS ##

   def _get_left_right_for_exterior_leaf(self, leaf):
      '''Get left and right flag counts for exterior leaf in spanner.'''
      spanner = self.spanner
      # lone
      if spanner._is_my_only_leaf(leaf):
         left, right = self._get_left_right_for_lone_leaf(leaf)
      # first
      elif spanner._is_my_first_leaf(leaf) or not leaf.prev:
         left = 0
         right = durtools.rational_to_flag_count(leaf.duration.written)
      # last
      elif spanner._is_my_last_leaf(leaf) or not leaf.next:
         left = durtools.rational_to_flag_count(leaf.duration.written)
         right = 0
      else:
         raise ValueError('leaf must be first or last in spanner.')
      return left, right

   def _get_left_right_for_interior_leaf(self, leaf):
      '''Interior leaves are neither first nor last in spanner.
      Interior leaves may be surrounded by beamable leaves.
      Interior leaves may be surrounded by unbeamable leaves.
      Four cases total for beamability of surrounding leaves.'''
      from abjad.tools import componenttools
      prev_written = leaf.prev.duration.written
      cur_written = leaf.duration.written
      next_written = leaf.next.duration.written
      prev_flag_count = durtools.rational_to_flag_count(prev_written)
      cur_flag_count = durtools.rational_to_flag_count(cur_written)
      next_flag_count = durtools.rational_to_flag_count(next_written)
      # [unbeamable leaf beamable]
      #if not leaf.prev.beam.beamable and leaf.next.beam.beamable:
      if not componenttools.is_beamable_component(leaf.prev) and \
         componenttools.is_beamable_component(leaf.next):
         left = cur_flag_count
         right = min(cur_flag_count, next_flag_count)
      # [beamable leaf unbeamable]
      #elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
      if componenttools.is_beamable_component(leaf.prev) and \
         not componenttools.is_beamable_component(leaf.next):
         left = min(cur_flag_count, prev_flag_count)
         right = cur_flag_count
      # [unbeamable leaf unbeamable]
      #elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
      elif not componenttools.is_beamable_component(leaf.prev) and \
         not componenttools.is_beamable_component(leaf.next):
         left = cur_flag_count
         right = cur_flag_count
      # [beamable leaf beamable]
      else:
         left = min(cur_flag_count, prev_flag_count)
         right = min(cur_flag_count, next_flag_count)
         if left != cur_flag_count and right != cur_flag_count:
            left = cur_flag_count
      return left, right

   def _get_left_right_for_lone_leaf(self, leaf):
      '''Get left and right flag counts for only leaf in spanner.'''
      spanner = self.spanner
      left, right = None, None
      if spanner.nibs == 'left':
         left = cur_flag_count
         right = 0
      elif spanner.nibs == 'right':
         left = 0
         right = cur_flag_count
      elif spanner.nibs == 'both':
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
      from abjad.tools import componenttools
      result = [ ]
      result.extend(_BeamSpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      #if leaf.beam.beamable:
      if componenttools.is_beamable_component(leaf):
         if spanner._is_exterior_leaf(leaf):
            left, right = self._get_left_right_for_exterior_leaf(leaf)
         else:
            left, right = self._get_left_right_for_interior_leaf(leaf)
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result

   def _right(self, leaf):
      '''Spanner format contribution to output right of leaf.'''
      from abjad.tools import componenttools
      result = [ ]
      spanner = self.spanner
      #if leaf.beam.beamable:
      if componenttools.is_beamable_component(leaf):
         # lone
         if spanner._is_my_only_leaf(leaf):
            if spanner.lone:
               result.append('[')
         # otherwise
         #elif spanner._is_my_first_leaf(leaf) or not leaf.prev or \
         #   not leaf.prev.beam.beamable:
         elif spanner._is_my_first_leaf(leaf) or not leaf.prev or \
            not componenttools.is_beamable_component(leaf.prev):
            result.append('[')
         # lone
         if spanner._is_my_only_leaf(leaf):
            if spanner.lone:
               result.append(']')
         # otherwise
         #elif spanner._is_my_last_leaf(leaf) or not leaf.next or \
         #   not leaf.next.beam.beamable:
         elif spanner._is_my_last_leaf(leaf) or not leaf.next or \
            not componenttools.is_beamable_component(leaf.next):
            result.append(']')
      return result
