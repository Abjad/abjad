# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import containertools


def get_measure_that_starts_with_container(container):
    '''Get measure that starts with `container`.

    Return measure or none.
    '''
    from abjad.tools import measuretools

    if isinstance(container, containertools.Container):
        contents = container._get_descendants_starting_with()
        contents = [x for x in contents if isinstance(x, measuretools.Measure)]
        if contents:
            return contents[0]
        raise MissingMeasureError
