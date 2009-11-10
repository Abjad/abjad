from abjad.container import Container
from abjad.exceptions import MeasureContiguityError
from abjad.exceptions import MissingMeasureError
from abjad.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.tools.iterate.naive_backward import naive_backward as \
   iterate_naive_backward
from abjad.tools.iterate.naive_forward import naive_forward as \
   iterate_naive_forward
from _get_contemporaneous_measure import _get_contemporaneous_measure


def _measure_get(component, direction):
   '''.. versionadded:: 1.1.1

   When `component` is voice, staff or other sequential context,
   and when `component` contains a measure, return first measure 
   in `component`.

   When `component` is voice, staff or other sequential context,
   and when `component` contains no measure, 
   raise :exc:`MissingMeasureError`. 

   When `component` is a measure and there is a measure immediately
   following `component`, return measure immediately following component.

   When `component` is a measure and there is not measure immediately
   following `component`, raise :exc:`MeasureContiguityError`.

   When `component` is a leaf and there is a measure in the parentage
   of `component`, return the measure in the parentage of `component`.

   When `component` is a leaf and there is no measure in the parentage
   of `component`, raise :exc:`MissingMeasureError`.
   '''

   if isinstance(component, _Leaf):
      for parent in component.parentage.parentage[1:]:
         if isinstance(parent, _Measure):
            return parent
      raise MissingMeasureError
   elif isinstance(component, _Measure):
      if direction == '_next':
         return component._navigator._nextNamesake
      elif direction == '_prev':
         return component._navigator._prevNamesake
      else:
         raise ValueError('direction must be _next or _prev.')
   elif isinstance(component, Container):
      return _get_contemporaneous_measure(component, direction)
   elif isinstance(component, (list, tuple)):
      if direction == '_next':
         measure_generator = iterate_naive_forward(component, _Measure)
      elif direction == '_prev':
         measure_generator = iterate_naive_backward(component, _Measure)
      else:
         raise ValueError('direction must be _next or _prev.')
      try:
         measure = measure_generator.next( )
         return measure
      except StopIteration:
         raise MissingMeasureError
   else:
      raise TypeError('"%s" is unknown Abjad component.' % component)
