from abjad.container import Container
from abjad.exceptions import MissingMeasureError
from abjad.measure.measure import _Measure


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
