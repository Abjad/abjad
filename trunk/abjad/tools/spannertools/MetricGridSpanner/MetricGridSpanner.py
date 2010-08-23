from abjad.tools.spannertools.MetricGridSpanner._MetricGridSpannerFormatInterface import _MetricGridSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools import mathtools


class MetricGridSpanner(Spanner):
   '''MetricGrid is a list of MetricStrips.'''

   def __init__(self, music, meters):
      Spanner.__init__(self, music)
      self._format = _MetricGridSpannerFormatInterface(self)
      self._meters = meters
      self.hide = False

   ## PRIVATE METHODS ##

   def _fuse_tied_leaves_within_measures(self):
      from abjad.tools import leaftools
      from abjad.tools import spannertools
      from abjad.tools import tietools
      ## fuse tied notes
      meters = self.meters
      #meter = meters.next( )
      meter, moffset, temp_hide = meters.next( )
      leaves_in_meter = [[]]
      leaf = self.leaves[0]
      ## group leaves by measure.
      while leaf:
         #if leaf.offset.start < meter.offset + meter.duration:
         if leaf.offset.start < moffset + meter.duration:
            leaves_in_meter[-1].append(leaf)
            leaf = leaf.next
         else:
            try:
               #meter = meters.next( )
               meter, moffset, temp_hide = meters.next( )
               leaves_in_meter.append([])
            except StopIteration:
               break
      ## group together leaves in same measure that are tied together.
      for leaves in leaves_in_meter:
         result = [[ ]]
         if 0 < len(leaves):
            #if leaves[0].tie.spanned:
            if tietools.is_component_with_tie_spanner_attached(leaves[0]):
               #sp = leaves[0].tie.spanner
               sp = spannertools.get_the_only_spanner_attached_to_component(
                  leaves[0], spannertools.TieSpanner)
            else:
               sp = None
         for l in leaves:
            #if l.tie.spanned and l.tie.spanner == sp:
            if tietools.is_component_with_tie_spanner_attached(l):
               if spannertools.get_the_only_spanner_attached_to_component(
                  l, spannertools.TieSpanner) == sp:
                  result[-1].append(l)
            else:
               #if l.tie.spanned:
               if tietools.is_component_with_tie_spanner_attached(l):
                  #sp = l.tie.spanner
                  sp = spannertools.get_the_only_spanner_attached_to_component(
                     l, spannertools.TieSpanner)
               else:
                  sp = None
               result.append([ ])
         ## fuse leaves 
         for r in result:
            ## keep last after graces, if any
            ## TODO: this is very hacky. Find better solution
            if 0 < len(r):
               #r[0].grace.after = r[-1].grace.after
               r[0].after_grace.extend(r[-1].after_grace)
            leaftools.fuse_leaves_big_endian(r)
         
   def _matching_meter(self, leaf):
      '''Return the MetricStrip for which meter.offset == leaf.offset'''
      #for m in self.meters:
      for m, moffset, temp_hide in self.meters:
         #if leaf.offset.start == m.offset: 
         if leaf.offset.start == moffset: 
            return m, temp_hide

   def _slicing_meters(self, leaf):
      '''Return the MetricStrip(s) that slices leaf, if any.'''
      #for m in self.meters:
      for m, moffset, temp_hide in self.meters:
         #if leaf.offset.start < m.offset:
         if leaf.offset.start < moffset:
            #if m.offset < leaf.offset.stop:
            if moffset < leaf.offset.stop:
               yield m, moffset, temp_hide
            else:
               break

   ## PUBLIC ATTRIBUTES ##

   @apply
   def meters( ):
      def fget(self):
         from abjad.tools.metertools import Meter
         i = 0
         moffset = 0
         prev_meter = None
         #while moffset < self.duration:
         while moffset < self.duration.prolated:
            m = self._meters[i % len(self._meters)]
            m = Meter(*m)
            ## new attribute
            #m.offset = moffset
            if prev_meter and prev_meter == m:
               #m.hide = True
               #m._temp_hide = True
               temp_hide = True
            else:
               temp_hide = False
            #yield m
            yield m, moffset, temp_hide
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
         leaves, [x[0].duration for x in self.meters], tie_after = True)
      self._fuse_tied_leaves_within_measures( )
