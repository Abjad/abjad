from abjad.beam.complex.format import _BeamComplexFormatInterface


class _BeamComplexDuratedFormatInterface(_BeamComplexFormatInterface):

#   def __init__(self, spanner):
#      _BeamComplexFormatInterface.__init__(self, spanner)

   ## PRIVATE METHODS ##

#   def _getLeftRightForExteriorLeaf(self, leaf):
#      '''Get left and right flag counts for exterior leaf in spanner.'''
#      spanner = self.spanner
#      # lone
#      if spanner._isMyOnlyLeaf(leaf):
#         left, right = self._getLeftRightForLoneLeaf(leaf)
#      # first
#      elif spanner._isMyFirstLeaf(leaf) or not leaf.prev:
#         left = 0
#         right = leaf.duration._flags
#      # last
#      elif spanner._isMyLastLeaf(leaf) or not leaf.next:
#         left = leaf.duration._flags
#         right = 0
#      else:
#         raise ValueError('leaf must be first or last in spanner.')
#      return left, right
#
#   def _getLeftRightForInteriorLeaf(self, leaf):
#      """'Interior' leaves are neither first nor last in spanner.
#         Interior leaves may be surrounded by beamable leaves.
#         Interior leaves may be surrounded by unbeamable leaves.
#         Four cases total for beamability of surrounding leaves."""
#      # [unbeamable leaf beamable]
#      if not leaf.prev.beam.beamable and leaf.next.beam.beamable:
#         left = leaf.duration._flags
#         right = min(leaf.duration._flags, leaf.next.duration._flags)
#      # [beamable leaf unbeamable]
#      elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
#         left = min(leaf.duration._flags, leaf.prev.duration._flags)
#         right = leaf.duration._flags
#      # [unbeamable leaf unbeamable]
#      elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
#         left = leaf.duration._flags
#         right = leaf.duration._flags
#      # [beamable leaf beamable]
#      else:
#         left = min(leaf.duration._flags, leaf.prev.duration._flags)
#         right = min(leaf.duration._flags, leaf.next.duration._flags)
#         if left != leaf.duration._flags and right != leaf.duration._flags:
#            left = leaf.duration._flags
#      return left, right
#
#   def _getLeftRightForLoneLeaf(self, leaf):
#      '''Get left and right flag counts for only leaf in spanner.'''
#      spanner = self.spanner
#      left, right = None, None
#      if spanner.nibs == 'left':
#         left = leaf.duration._flags
#         right = 0
#      elif spanner.nibs == 'right':
#         left = 0
#         right = leaf.duration._flags
#      elif spanner.nibs == 'both':
#         left = leaf.duration._flags
#         right = leaf.duration._flags
#      elif spanner.nibs == 'neither':
#         left = None
#         right = None
#      else:
#         raise ValueError('nibs must be left, right, both or neither.')
#      return left, right

   ## PUBLIC METHODS ##

   def before(self, leaf):
      '''Spanner format contribution to output before leaf.'''
      result = [ ]
      spanner = self.spanner
      if leaf.beam.beamable:
         if spanner._isExteriorLeaf(leaf):
            left, right = self._getLeftRightForExteriorLeaf(leaf)
         # just right of span gap
         elif spanner._durationOffsetInMe(leaf) in spanner._spanPoints and not \
            (spanner._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            spanner._spanPoints):
            assert isinstance(spanner.span, int)
            left = spanner.span
            right = leaf.duration._flags
         # just left of span gap
         elif spanner._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            spanner._spanPoints and not spanner._durationOffsetInMe(leaf) in \
            spanner._spanPoints:
            assert isinstance(spanner.span, int)
            left = leaf.duration._flags
            right = spanner.span
         else:
            left, right = self._getLeftRightForInteriorLeaf(leaf)
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result

#   def right(self, leaf):
#      '''Spanner format contribution to output right of leaf.'''
#      result = [ ]
#      spanner = self.spanner
#      if leaf.beam.beamable:
#         # lone
#         if spanner._isMyOnlyLeaf(leaf):
#            if spanner.lone:
#               result.append('[')
#         # otherwise
#         elif spanner._isMyFirstLeaf(leaf) or not leaf.prev or \
#            not leaf.prev.beam.beamable:
#            result.append('[')
#         # lone
#         if spanner._isMyOnlyLeaf(leaf):
#            if spanner.lone:
#               result.append(']')
#         # otherwise
#         elif spanner._isMyLastLeaf(leaf) or not leaf.next or \
#            not leaf.next.beam.beamable:
#            result.append(']')
#      return result
