from abjad.core.spanner import _Spanner
from abjad.measure.meter import _Meter
from abjad.skip.skip import Skip
from abjad.tie.spanner import Tie
from abjad.helpers.leaf_split import leaf_split_binary, leaf_split
from abjad.helpers.leaves_fuse import leaves_fuse_binary
from abjad.duration.rational import Rational

class MetricGrid(_Spanner):
   '''MetricGrid is a list of MetricStrips.'''
   def __init__(self, music, meters):
      _Spanner.__init__(self, music)
      self._setupMeters(meters )
#      self.offset ?

   def _setupMeters(self, meters):
      ''' __init__ helper to preformat Meters.'''
      result = [ ] 
      i = 0
      mdur = 0
      while mdur < self.duration:
         m = meters[i % len(meters)]
         m = _Meter(*m)
         result.append(m)
         mdur += m.duration
         i += 1
      self.meters = result

      ### preformat meters
      if self.meters:
         meter_ref = self.meters[0]
      for m in self.meters[1:]:
         if m == meter_ref:
            m.hide = True
         else:
            meter_ref = m


   def splitOnBar(self):
      '''Destructive slice of notes to metric grid.'''
      for leaf in self:
         if not leaf.tie.spanner:
            t = Tie(leaf)
            t._captureLeafTies( )
         meters = self._slicingMeters(leaf)
         for meter in meters:
            moffset = self._meterOffset(meter)
            splitdur = moffset - leaf.offset
            ### if splitdur not m / 2**n
            if not splitdur._denominator & (splitdur._denominator - 1):
               leaves_splitted = leaf_split_binary(splitdur, leaf)
            else:
               leaves_splitted = leaf_split(splitdur, leaf)
#            try:
#               leaves_splitted = leaf_split_binary(splitdur, leaf)
#            except ValueError: ### if not binary duration
#               leaves_splitted = leaf_split(splitdur, leaf)
            
            ### TODO put this in its own function.
            ### fuse tied leaves in meter
            leaves = self._leavesStrictlyBoundedByMeter(meter)
            if leaves:
               result = [[leaves[0]]]
               sp = leaves[0].tie.spanner
               for l in leaves[1:]:
                  if l.tie.spanner == sp:
                     result[-1].append(l)
                  else:
                     sp = l.tie.spanner
                     result.append([])
               for r in result:
                  leaves_fuse_binary(r)

   def _slicingMeters(self, leaf):
      '''Return the MetricStrip(s) that slices leaf, if any.'''
      result = [ ]
      offsetReference = self[0].offset
      offsetMeter = offsetReference
      for m in self.meters:
         if leaf.offset < offsetMeter:
            if leaf.offset + leaf.duration.prolated > offsetMeter:
               result.append( m )
            else:
               break
         offsetMeter += m.duration
      return result

   def _matchingMeter(self, leaf):
      '''Return the MetricStrip for which meter.offset == leaf.offset
      and leaf.offset + leaf.duration < meter.next.offset.'''
      offsetReference = self[0].offset
      offsetMeter = offsetReference
      for m in self.meters:
         if leaf.offset == offsetMeter: 
         #   if leaf.offset + leaf.duration.prolated < m.duration:
            return m
         offsetMeter += m.duration


   ### TO meter ATTRIBUTES ###

   def _meterOffset(self, meter):
      '''Return the offset time of give meter.'''
      offset = 0 
      for m in self.meters:
         if m is meter:
            break
         offset += m.duration
      return offset

   def _leavesStrictlyBoundedByMeter(self, meter):
      '''Return leaves spanned that are completely bound by given meter. 
      i.e. both offset and offset+duration fall within the meter.'''
      result = [ ]
      meterOffset = self._meterOffset(meter)
      for l in self:
         if l.offset >= meterOffset and \
            l.offset + l.duration.prolated <= meterOffset + meter.duration:
            result.append(l)
      return result
         

   def _strictlyBoundedLeaves(self, meter):
      pass

   ### FORMATTING ### 

   def _before(self, leaf):
      result = [ ]
      meter = self._matchingMeter(leaf)
      if meter and not meter.hide:
         result.append(meter.lily)
         #return result
      m = self._slicingMeters(leaf)
#      if m:
      m = [meter for meter in m if not meter.hide]
      if m:
         result.append('<<')
         for meter in m:
            if not meter.hide:
               s = Skip( 1 )
               s.duration.multiplier = self._meterOffset(meter) - leaf.offset
               s.formatter.right.append(meter.lily)
               #result.append( '<<\n\t%s' % Sequential([s]).format )
               result.append( '{ %s }' % s.format )
      return result

   def _after(self, leaf):
      result = [ ]
      m = self._slicingMeters(leaf)
#      if m:
      if any([not meter.hide for meter in m]):
         result.append( '>>' )
      return result

