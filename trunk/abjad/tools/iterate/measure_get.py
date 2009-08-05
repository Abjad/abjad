from abjad.container import Container
from abjad.exceptions import MeasureContiguityError
from abjad.exceptions import MissingMeasureError
from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.tools.iterate.backwards import backwards as iterate_backwards
from abjad.tools.iterate.naive import naive as iterate_naive


def _measure_get(component, direction):
   '''When `component` is voice, staff or other sequential context,
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
         measure_generator = iterate_naive(component, _Measure)
      elif direction == '_prev':
         measure_generator = iterate_backwards(component, _Measure)
      else:
         raise ValueError('direction must be _next or _prev.')
      try:
         measure = measure_generator.next( )
         return measure
      except StopIteration:
         raise MissingMeasureError
   else:
      raise TypeError('"%s" is unknown Abjad component.' % component)


def _get_contemporaneous_measure(container, direction):
   '''Return measure in container starting at same moment as container.'''

   if isinstance(container, Container):
      if direction == '_next':
         contents = container._navigator._contemporaneousStartContents
      elif direction == '_prev':
         contents = container._navigator._contemporaneousStopContents
      else:
         raise ValueError("direction must be '_next' or '_prev'.")
      contents = [x for x in contents if isinstance(x, _Measure)]
      if contents:
         return contents[0]
      raise MissingMeasureError
