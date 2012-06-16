from abjad.tools.timeintervaltools import *


def test_TimeIntervalTreeDictionary_storage_format_01():

    a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
    b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
    c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
    d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])

    treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
    
    r'''
    timeintervaltools.TimeIntervalTreeDictionary({
        'a': timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(
                Offset(0, 1),
                Offset(1, 1),
                {
                    'name': 'a',
                }),
            ]),
        'c': timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(
                Offset(0, 1),
                Offset(3, 1),
                {
                    'name': 'c',
                }),
            ]),
        'b': timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(
                Offset(1, 1),
                Offset(2, 1),
                {
                    'name': 'b',
                }),
            ]),
        'd': timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(
                Offset(2, 1),
                Offset(3, 1),
                {
                    'name': 'd',
                }),
            ]),
        })
    '''

    assert treedict.storage_format == "timeintervaltools.TimeIntervalTreeDictionary({\n\t'a': timeintervaltools.TimeIntervalTree([\n\t\ttimeintervaltools.TimeInterval(\n\t\t\tOffset(0, 1),\n\t\t\tOffset(1, 1),\n\t\t\t{\n\t\t\t\t'name': 'a',\n\t\t\t}),\n\t\t]),\n\t'c': timeintervaltools.TimeIntervalTree([\n\t\ttimeintervaltools.TimeInterval(\n\t\t\tOffset(0, 1),\n\t\t\tOffset(3, 1),\n\t\t\t{\n\t\t\t\t'name': 'c',\n\t\t\t}),\n\t\t]),\n\t'b': timeintervaltools.TimeIntervalTree([\n\t\ttimeintervaltools.TimeInterval(\n\t\t\tOffset(1, 1),\n\t\t\tOffset(2, 1),\n\t\t\t{\n\t\t\t\t'name': 'b',\n\t\t\t}),\n\t\t]),\n\t'd': timeintervaltools.TimeIntervalTree([\n\t\ttimeintervaltools.TimeInterval(\n\t\t\tOffset(2, 1),\n\t\t\tOffset(3, 1),\n\t\t\t{\n\t\t\t\t'name': 'd',\n\t\t\t}),\n\t\t]),\n\t})"
