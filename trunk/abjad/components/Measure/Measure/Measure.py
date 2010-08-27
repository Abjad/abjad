from abjad.components.Measure._Measure import _Measure
from abjad.components.Measure.Measure._RigidMeasureDurationInterface import \
   _RigidMeasureDurationInterface
from abjad.components.Measure.Measure._RigidMeasureFormatter import _RigidMeasureFormatter
from abjad.tools.metertools import Meter
from abjad.tools import durtools
from abjad.tools import marktools


class Measure(_Measure):

   def __init__(self, meter, music = None, **kwargs):
      from abjad.components import Staff
      _Measure.__init__(self, music)
      self._duration = _RigidMeasureDurationInterface(self)
      #self._explicit_meter = None
      self._formatter = _RigidMeasureFormatter(self)
      #self.meter.forced = Meter(meter)
      meter = Meter(meter)
      numerator, denominator = meter.numerator, meter.denominator
      #meter = marktools.TimeSignatureMark(numerator, denominator)(Staff, self)
      #self._explicit_meter = meter
      self._attach_explicit_meter(numerator, denominator)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __delitem__(self, i):
      '''Container deletion with meter adjustment.'''
      try:
         #old_denominator = self.meter.forced.denominator
         old_denominator = self.meter.effective.denominator
      except AttributeError:
         pass
      _Measure.__delitem__(self, i)
      try:
         naive_meter = self.duration.preprolated
         better_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            naive_meter, old_denominator)
         #self.meter.forced = Meter(better_meter)
         self._attach_explicit_meter(*better_meter)
      except (AttributeError, UnboundLocalError):
         pass

#   ## PRIVATE METHODS ##
#
#   #def _attach_explicit_meter(self, numerator, denominator, partial = None):
#   def _attach_explicit_meter(self, *args, **kwargs):
#      from abjad.components import Staff
#      from abjad.tools import marktools
#      from abjad.tools import metertools
#      if len(args) == 1 and isinstance(args[0], marktools.TimeSignatureMark):
#         new_explicit_meter = args[0]
#      elif len(args) == 1 and isinstance(args[0], metertools.Meter):
#         numerator, denominator = args[0].numerator, args[0].denominator
#         new_explicit_meter = marktools.TimeSignatureMark(numerator, denominator)
#      elif len(args) == 2:
#         numerator, denominator = args
#         new_explicit_meter = marktools.TimeSignatureMark(numerator, denominator)
#      partial = kwargs.get('partial', None)
#      if partial is not None:
#         raise Exception('implement partial meter.')
#      if self._explicit_meter is not None:
#         self._explicit_meter.detach_mark( )
#      new_explicit_meter(Staff, self)
#      self._explicit_meter = new_explicit_meter
