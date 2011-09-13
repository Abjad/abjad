from abjad.tools.containertools.Container import Container
from abjad.tools.measuretools.Measure import Measure
from abjad.exceptions import MissingMeasureError


def _get_contemporaneous_measure(container, direction):
    '''Return measure in container starting at same moment as container.'''

    if isinstance(container, Container):
        if direction == '_next':
            contents = container._navigator._contemporaneous_start_contents
        elif direction == '_prev':
            contents = container._navigator._contemporaneous_stop_contents
        else:
            raise ValueError("direction must be '_next' or '_prev'.")
        contents = [x for x in contents if isinstance(x, Measure)]
        if contents:
            return contents[0]
        raise MissingMeasureError
