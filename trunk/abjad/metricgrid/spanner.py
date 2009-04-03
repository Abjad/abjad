from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.helpers.leaf_split import leaf_split
from abjad.helpers.leaf_split_binary import leaf_split_binary
from abjad.helpers.leaves_fuse_binary import leaves_fuse_binary
from abjad.meter.meter import Meter
from abjad.rational.rational import Rational
from abjad.skip.skip import Skip
from abjad.spanner.spanner import Spanner
from abjad.tie.spanner import Tie


class MetricGrid(Spanner):
   '''MetricGrid is a list of MetricStrips.'''

   def __init__(self, music, meters):
      Spanner.__init__(self, music)
      self._meters = meters
      self.hide = False

   ## PRIVATE ATTRIBUTES ## 

   def _after(self, leaf):
      result = [ ]
      if hasattr(self, '_slicingMetersFound'):
         delattr(self, '_slicingMetersFound')
         result.append('>>')
      return result

   ##FIXME: formatting is ridiculously slow. 
   ##       find a way to make it faster.
   ## Tue Jan 13 12:05:43 EST 2009 [VA] using _slicingMetersFound boolean
   ## flag now to improve performance time. Better but still not perfect. 
   ## Is metricgrid a good candidate for the UpdateInterface?

   def _before(self, leaf):
      result = [ ]
      if not self.hide:
         meter = self._matchingMeter(leaf)
         if meter and not getattr(meter, '_temp_hide', False):
            result.append(meter.format)
         m = self._slicingMeters(leaf)
         m = [meter for meter in m if not getattr(meter, '_temp_hide', False)]
         if m:
            ## set self._slicingMetersFound as temporary flag so that 
            ## self._after does not have to recompute _slicingMeters( )
            self._slicingMetersFound = True
            result.append('<<')
            for meter in m:
               s = Skip(Rational(1))
               s.duration.multiplier = meter.offset - leaf.offset.score
               ## TODO: Avoid _AnnotationsInterface in _MetricGrid ##
               s.annotations.right.append(meter.format)
               result.append( '{ %s }' % s.format )
      return result

   ## PRIVATE METHODS ##

   def _fuseTiedLeavesWithinMeasures(self):
      ## fuse tied notes
      meters = self.meters
      meter = meters.next( )
      leaves_in_meter = [[]]
      leaf = self.leaves[0]
      ## group leaves by measure.
      while leaf:
         if leaf.offset.score < meter.offset + meter.duration:
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
            leaves_fuse_binary(r)
         
   def _matchingMeter(self, leaf):
      '''Return the MetricStrip for which meter.offset == leaf.offset'''
      for m in self.meters:
         if leaf.offset.score == m.offset: 
            return m

   def _slicingMeters(self, leaf):
      '''Return the MetricStrip(s) that slices leaf, if any.'''
      for m in self.meters:
         if leaf.offset.score < m.offset:
            if leaf.offset.score + leaf.duration.prolated > m.offset:
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
      leaf = self.leaves[0]
      meters = self.meters
      meter = meters.next( )
      while leaf:
         if leaf.offset.score < meter.offset:
            if leaf.offset.score + leaf.duration.prolated > meter.offset and \
               self.splittingCondition(leaf):
               ## will split
               if not leaf.tie.parented:
                  Tie(leaf)
               splitdur = meter.offset - leaf.offset.score
               ## if splitdur not m / 2**n
               if _is_power_of_two(splitdur._denominator):
                  leaves_splitted = leaf_split_binary(leaf, splitdur)
                  leaf = leaves_splitted[1][0]
               else:
                  leaves_splitted = leaf_split(leaf, splitdur)
                  leaf = leaves_splitted[1].leaves[0]
            else:
               ## only advance if we have not split.
               leaf = leaf.next
         else:
            try:
               meter = meters.next( )
            except StopIteration:
               break 
      self._fuseTiedLeavesWithinMeasures( )
