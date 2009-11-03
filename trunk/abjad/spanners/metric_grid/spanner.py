from abjad.meter import Meter
from abjad.spanners.metric_grid.format import _MetricGridSpannerFormatInterface
from abjad.spanners.spanner.spanner import Spanner
from abjad.spanners.tie import Tie
from abjad.tools import mathtools


class MetricGrid(Spanner):
   '''MetricGrid is a list of MetricStrips.'''

   def __init__(self, music, meters):
      Spanner.__init__(self, music)
      self._format = _MetricGridSpannerFormatInterface(self)
      self._meters = meters
      self.hide = False

   ## PRIVATE METHODS ##

   def _fuseTiedLeavesWithinMeasures(self):
      from abjad.tools import fuse
      ## fuse tied notes
      meters = self.meters
      meter = meters.next( )
      leaves_in_meter = [[]]
      leaf = self.leaves[0]
      ## group leaves by measure.
      while leaf:
         if leaf.offset.prolated.start < meter.offset + meter.duration:
            leaves_in_meter[-1].append(leaf)
            leaf = leaf.next
         else:
            try:
               meter = meters.next( )
               leaves_in_meter.append([])
            except StopIteration:
               break
      ## group together leaves in same measure that are tied together.
      for leaves in leaves_in_meter:
         result = [[ ]]
         if len(leaves) > 0:
            if leaves[0].tie.spanned:
               sp = leaves[0].tie.spanner
            else:
               sp = None
         for l in leaves:
            if l.tie.spanned and l.tie.spanner == sp:
               result[-1].append(l)
            else:
               if l.tie.spanned:
                  sp = l.tie.spanner
               else:
                  sp = None
               result.append([ ])
         ## fuse leaves 
         for r in result:
            ## keep last after graces, if any
            ## TODO: this is very hacky. Find better solution
            if len(r) > 0:
               r[0].grace.after = r[-1].grace.after
            fuse.leaves_by_reference(r)
         
   def _matchingMeter(self, leaf):
      '''Return the MetricStrip for which meter.offset == leaf.offset'''
      for m in self.meters:
         if leaf.offset.prolated.start == m.offset: 
            return m

   def _slicingMeters(self, leaf):
      '''Return the MetricStrip(s) that slices leaf, if any.'''
      for m in self.meters:
         if leaf.offset.prolated.start < m.offset:
            if leaf.offset.prolated.stop > m.offset:
               yield m 
            else:
               break

   ## PUBLIC ATTRIBUTES ##

   @apply
   def meters( ):
      def fget(self):
         i = 0
         moffset = 0
         prev_meter = None
         #while moffset < self.duration:
         while moffset < self.duration.prolated:
            m = self._meters[i % len(self._meters)]
            m = Meter(*m)
            ## new attribute
            m.offset = moffset
            if prev_meter and prev_meter == m:
               #m.hide = True
               m._temp_hide = True
            yield m
            moffset += m.duration
            i += 1
            prev_meter = m
      def fset(self, meters):
         assert isinstance(meters, list)
         self._meters = meters
      return property(**locals( ))

   ## PUBLIC METHODS ##
         
   def splittingCondition(self, leaf):
      '''User definable conditioning function.'''
      return True

   def splitOnBar(self):
      from abjad.tools import partition
#      from abjad.tools import split
#      leaf = self.leaves[0]
#      meters = self.meters
#      meter = meters.next( )
#      while leaf:
#         if leaf.offset.prolated.start < meter.offset:
#            if leaf.offset.prolated.stop > meter.offset and \
#               self.splittingCondition(leaf):
#               ## will split
#               if not leaf.tie.parented:
#                  Tie(leaf)
#               splitdur = meter.offset - leaf.offset.prolated.start
#               #leaves_splitted = split.leaf_at_duration(leaf, splitdur)
#               leaves_splitted = split.unfractured_at_duration(leaf, splitdur)
#               leaf = leaves_splitted[0][0]
#            else:
#               ## only advance if we have not split.
#               leaf = leaf.next
#         else:
#            try:
#               meter = meters.next( )
#            except StopIteration:
#               break 
      leaves = [leaf for leaf in self.leaves if self.splittingCondition(leaf)]
      partition.cyclic_unfractured_by_durations(leaves, [x.duration for x in self.meters], tie_after = True)
      self._fuseTiedLeavesWithinMeasures( )
