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
               left = leaf.beam._flags
               right = 0
            #elif spanner.lone == 'right':
            elif spanner.nibs == 'right':
               left = 0
               right = leaf.beam._flags
            #elif spanner.lone == 'both':
            elif spanner.nibs == 'both':
               left = leaf.beam._flags
               right = leaf.beam._flags
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
            right = leaf.beam._flags
         # last
         elif spanner._isMyLastLeaf(leaf) or not leaf.next:
            left = leaf.beam._flags
            right = 0
         # just right of span gap
         elif spanner._durationOffsetInMe(leaf) in spanner._spanPoints and not \
            (spanner._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            spanner._spanPoints):
            assert isinstance(spanner.span, int)
            left = spanner.span
            right = leaf.beam._flags
         # just left of span gap
         elif spanner._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            spanner._spanPoints and not spanner._durationOffsetInMe(leaf) in \
            spanner._spanPoints:
            assert isinstance(spanner.span, int)
            left = leaf.beam._flags
            right = spanner.span
         # [unbeamable leaf beamable]
         elif not leaf.prev.beam.beamable and leaf.next.beam.beamable:
            left = leaf.beam._flags
            right = min(leaf.beam._flags, leaf.next.beam._flags)
         # [beamable leaf unbeamable]
         elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
            left = min(leaf.beam._flags, leaf.prev.beam._flags)
            right = leaf.beam._flags
         # [unbeamable leaf unbeamable]
         elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
            left = leaf.beam._flags
            right = leaf.beam._flags
         # [beamable leaf beamable]
         else:
            left = min(leaf.beam._flags, leaf.prev.beam._flags)
            right = min(leaf.beam._flags, leaf.next.beam._flags)
            if left != leaf.beam._flags and right != leaf.beam._flags:
               left = leaf.beam._flags
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
