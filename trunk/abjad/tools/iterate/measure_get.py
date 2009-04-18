from abjad.container.container import Container
from abjad.exceptions.exceptions import MeasureContiguityError
from abjad.exceptions.exceptions import MissingMeasureError
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
      candidate = getattr(component._navigator, direction)
      if candidate is None:
         raise StopIteration
      elif isinstance(candidate, _Leaf):
         raise MeasureContiguityError
      elif isinstance(candidate, _Measure):
         return candidate
      elif isinstance(candidate, Container):
         return _get_contemporaneous_measure(candidate, direction)
      else:
         raise TypeError('unknown Abjad component.')
   elif isinstance(component, Container):
      return _get_contemporaneous_measure(component, direction)
   else:
      raise TypeError('unknown Abjad component.')


def _get_contemporaneous_measure(container, direction):
   '''Return measure in contents of container 
      that starts at same moment as container.'''

   if isinstance(container, Container):
      if not container.parallel:
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
   raise TypeError('measure-iterate sequential containers only.')
