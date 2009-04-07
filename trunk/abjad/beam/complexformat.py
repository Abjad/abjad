from abjad.beam.format import _BeamSpannerFormatInterface


class _ComplexBeamSpannerFormatInterface(_BeamSpannerFormatInterface):

   def __init__(self, spanner):
      _BeamSpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def before(self, leaf):
      '''Spanner format contribution to output before leaf.'''
      result = [ ]
      result.extend(_BeamSpannerFormatInterface.before(self, leaf))
      spanner = self.spanner
      if leaf.beam.beamable:
         left, right = None, None
         # lone
         if spanner._isMyOnlyLeaf(leaf):
            #elif spanner.lone == 'left':
            if spanner.nibs == 'left':
               left = leaf.duration._flags
               right = 0
            #elif spanner.lone == 'right':
            elif spanner.nibs == 'right':
               left = 0
               right = leaf.duration._flags
            #elif spanner.lone == 'both':
            elif spanner.nibs == 'both':
               left = leaf.duration._flags
               right = leaf.duration._flags
            #if spanner.lone in (True, False):
            elif spanner.nibs == 'neither':
               left = None
               right = None
            else:
               #raise ValueError('lone must be left, right or both.')
               raise ValueError('nibs must be left, right, both or neither.')
         # first
         elif spanner._isMyFirstLeaf(leaf) or not leaf.prev:
            left = 0
            right = leaf.duration._flags
         # last
         elif spanner._isMyLastLeaf(leaf) or not leaf.next:
            left = leaf.duration._flags
            right = 0
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
         # [unbeamable leaf beamable]
         elif not leaf.prev.beam.beamable and leaf.next.beam.beamable:
            left = leaf.duration._flags
            right = min(leaf.duration._flags, leaf.next.duration._flags)
         # [beamable leaf unbeamable]
         elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
            left = min(leaf.duration._flags, leaf.prev.duration._flags)
            right = leaf.duration._flags
         # [unbeamable leaf unbeamable]
         elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
            left = leaf.duration._flags
            right = leaf.duration._flags
         # [beamable leaf beamable]
         else:
            left = min(leaf.duration._flags, leaf.prev.duration._flags)
            right = min(leaf.duration._flags, leaf.next.duration._flags)
            if left != leaf.duration._flags and right != leaf.duration._flags:
               left = leaf.duration._flags
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result

   def right(self, leaf):
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
