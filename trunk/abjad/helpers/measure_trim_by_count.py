from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.measure import _Measure
from abjad.measure.rigid.measure import RigidMeasure


## TODO: Reimplement as measure_trim_by_count(t[1:3]) ######
##       Avoid ghetto slicing interface implemented here. ##

def measure_trim_by_count(measure, start, stop = 'unused'):
   '''When 'stop' is 'unusued', delete component at index 'start'.
      When 'stop' is set, delete components from 'start' to 'stop'.
      Measure may be anonymous, dynamic, rigid, etc.
      When 'measure' is rigid, change meter as appropriate.'''

   if not isinstance(measure, _Measure):
      raise TypeError('must be Abjad measure.')

   try:
      old_denominator = measure.meter.forced.denominator
   except AttributeError:
      pass

   if stop != 'unused':
      assert not (start == 0 and (stop is None or stop >= len(measure)))
   if stop == 'unused':
      del(measure[start])
   else:
      del(measure[start : stop])

   try:
      naive_meter = measure.duration.preprolated
      better_meter = _in_terms_of(naive_meter, old_denominator)
      measure.meter = better_meter
   except (AttributeError, UnboundLocalError):
      pass
