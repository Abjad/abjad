from abjad.container import Container
from abjad.rational import Rational
from abjad.skip import Skip
from abjad.spanner.format import _SpannerFormatInterface


class _MetricGridSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      spanner = self.spanner
      if hasattr(spanner, '_slicingMetersFound'):
         delattr(spanner, '_slicingMetersFound')
         result.append('>>')
      return result

   ##FIXME: formatting is ridiculously slow. 
   ##       find a way to make it faster.
   ## Tue Jan 13 12:05:43 EST 2009 [VA] using _slicingMetersFound boolean
   ## flag now to improve performance time. Better but still not perfect. 
   ## Is metricgrid a good candidate for the UpdateInterface?

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      spanner = self.spanner
      if not spanner.hide:
         meter = spanner._matchingMeter(leaf)
         if meter and not getattr(meter, '_temp_hide', False):
            result.append(meter.format)
         m = spanner._slicingMeters(leaf)
         m = [meter for meter in m if not getattr(meter, '_temp_hide', False)]
         if m:
            ## set spanner._slicingMetersFound as temporary flag so that 
            ## spanner._after does not have to recompute _slicingMeters( )
            spanner._slicingMetersFound = True
            result.append('<<')
            for meter in m:
               s = Skip(Rational(1))
               s.duration.multiplier = meter.offset - leaf.offset.prolated.start
               s.meter.forced = meter
               container = Container([s])
               result.append(container.format)
      return result
