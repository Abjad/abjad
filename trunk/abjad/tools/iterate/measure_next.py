from abjad.tools.iterate.measure_get import _measure_get


def measure_next(component):
   '''When component is voice, staff or other sequential context,
      return very first measure in component;
      else raise MissingMeasureError.

      When component is measure, return measure immediately following;
      else raise MeasureContiguityError.'''

   return _measure_get(component, '_next')
