from abjad.container import Container
from abjad.exceptions import MeasureContiguityError
from abjad.exceptions import MissingMeasureError
from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure


def _measure_get(component, direction):
   '''When component is voice, staff or other sequential context,
      return very first measure in component;
      else raise MissingMeasureError.

      When component is measure, return measure immediately following;
      else raise MeasureContiguityError.'''

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
   elif isinstance(component, Container):
      return _get_contemporaneous_measure(component, direction)
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
