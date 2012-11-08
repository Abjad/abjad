from abjad.tools import componenttools
from abjad.tools import containertools


def get_measure_that_starts_with_container(container):
    '''.. versionadded:: 2.11

    Get measure that starts with `container`.

    Return measure or none.
    '''
    from abjad.tools import measuretools

    if isinstance(container, containertools.Container):
        contents = componenttools.get_improper_descendents_of_component_that_start_with_component(container)
        contents = [x for x in contents if isinstance(x, measuretools.Measure)]
        if contents:
            return contents[0]
        raise MissingMeasureError
