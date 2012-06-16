from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import TimeInterval, TimeIntervalTree


def test_TimeIntervalTree_storage_format_01():

    a = TimeInterval(Offset(-1, 1), Offset(3, 1), {
        'a': 1, 'b': 2, 't': TimeInterval(Offset(2, 1), Offset(3, 1), {'x': 'b'})})
    b = TimeInterval(Offset(0, 1), Offset(1, 1), {'x': 'y'})
    tree = TimeIntervalTree([a, b])

    r'''
    timeintervaltools.TimeIntervalTree([
        timeintervaltools.TimeInterval(
            Offset(-1, 1),
            Offset(3, 1),
            {
                'a': 1,
                'b': 2,
                't': timeintervaltools.TimeInterval(
                    Offset(2, 1),
                    Offset(3, 1),
                    {
                        'x': 'b',
                    }),
            }),
        timeintervaltools.TimeInterval(
            Offset(0, 1),
            Offset(1, 1),
            {
                'x': 'y',
            }),
        ])
    '''

    assert tree.storage_format == "timeintervaltools.TimeIntervalTree([\n\ttimeintervaltools.TimeInterval(\n\t\tOffset(-1, 1),\n\t\tOffset(3, 1),\n\t\t{\n\t\t\t'a': 1,\n\t\t\t'b': 2,\n\t\t\t't': timeintervaltools.TimeInterval(\n\t\t\t\tOffset(2, 1),\n\t\t\t\tOffset(3, 1),\n\t\t\t\t{\n\t\t\t\t\t'x': 'b',\n\t\t\t\t}),\n\t\t}),\n\ttimeintervaltools.TimeInterval(\n\t\tOffset(0, 1),\n\t\tOffset(1, 1),\n\t\t{\n\t\t\t'x': 'y',\n\t\t}),\n\t])"
