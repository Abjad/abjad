from abjad.spanners.MetricGrid._MetricGridSpannerFormatInterface import \
   _MetricGridSpannerFormatInterface
from abjad.spanners.Spanner import Spanner
from abjad.spanners.Tie import Tie
from abjad.tools import mathtools


class MetricGrid(Spanner):
   '''MetricGrid is a list of MetricStrips.'''

   def __init__(self, music, meters):
      Spanner.__init__(self, music)
      self._format = _MetricGridSpannerFormatInterface(self)
      self._meters = meters
      self.hide = False

   ## PRIVATE METHODS ##

   def _fuse_tied_leaves_within_measures(self):
      from abjad.tools import leaftools
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
            leaftools.fuse_leaves_big_endian(r)
         
   def _matching_meter(self, leaf):
      '''Return the MetricStrip for which meter.offset == leaf.offset'''
      for m in self.meters:
         if leaf.offset.prolated.start == m.offset: 
            return m

   def _slicing_meters(self, leaf):
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
         from abjad.marks import Meter
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
         
   def splitting_condition(self, leaf):
      '''User definable conditioning function.'''
      return True

   def split_on_bar(self):
      from abjad.tools import componenttools
      leaves = [leaf for leaf in self.leaves if self.splitting_condition(leaf)]
      componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
         leaves, [x.duration for x in self.meters], tie_after = True)
      self._fuse_tied_leaves_within_measures( )
