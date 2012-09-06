from abjad.tools import componenttools
from abjad.tools import containertools


# TODO: make public
def _get_contemporaneous_measure(container, direction):
    '''Return measure in container starting at same moment as container.
    '''
    from abjad.tools import measuretools

    if isinstance(container, containertools.Container):
        if direction == '_next':
            contents = componenttools.get_improper_descendents_of_component_that_start_with_component(
                container)
        elif direction == '_prev':
            contents = componenttools.get_improper_descendents_of_component_that_stop_with_component(
                container)
        else:
            raise ValueError("direction must be '_next' or '_prev'.")
        contents = [x for x in contents if isinstance(x, measuretools.Measure)]
        if contents:
            return contents[0]
        raise MissingMeasureError
