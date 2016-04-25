# -*- coding: utf-8 -*-


def get_measure_that_stops_with_container(container):
    '''Get measure that stops with `container`.

    Returns measure or none.
    '''
    from abjad.tools import scoretools

    if isinstance(container, scoretools.Container):
        contents = container._get_descendants_stopping_with()
        contents = [x for x in contents if isinstance(x, scoretools.Measure)]
        if contents:
            return contents[0]
        raise MissingMeasureError
