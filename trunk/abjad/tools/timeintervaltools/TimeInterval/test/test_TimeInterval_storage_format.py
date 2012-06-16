from abjad.tools.durationtools import Offset
from abjad.tools import timeintervaltools


def test_TimeInterval_storage_format_01():

    t = timeintervaltools.TimeInterval(0, 1, {
        'a': timeintervaltools.TimeInterval(3, 4, {'x': 'y'}), 'b': 3
    })

    r'''
    timeintervaltools.TimeInterval(
        Offset(0, 1),
        Offset(1, 1),
        {
            'a': timeintervaltools.TimeInterval(
                Offset(3, 1),
                Offset(4, 1),
                {
                    'x': 'y',
                }),
            'b': 3,
        })
    '''

    assert t.storage_format == "timeintervaltools.TimeInterval(\n\tOffset(0, 1),\n\tOffset(1, 1),\n\t{\n\t\t'a': timeintervaltools.TimeInterval(\n\t\t\tOffset(3, 1),\n\t\t\tOffset(4, 1),\n\t\t\t{\n\t\t\t\t'x': 'y',\n\t\t\t}),\n\t\t'b': 3,\n\t})"
