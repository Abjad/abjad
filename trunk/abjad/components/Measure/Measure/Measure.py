from abjad.components.Measure._Measure import _Measure
from abjad.tools.metertools import Meter
from abjad.tools import durtools
from abjad.tools import marktools


class Measure(_Measure):

   def __init__(self, meter, music = None, **kwargs):
      _Measure.__init__(self, music)
      meter = Meter(meter)
      numerator, denominator = meter.numerator, meter.denominator
      self._attach_explicit_meter(numerator, denominator)
      self._initialize_keyword_values(**kwargs)
