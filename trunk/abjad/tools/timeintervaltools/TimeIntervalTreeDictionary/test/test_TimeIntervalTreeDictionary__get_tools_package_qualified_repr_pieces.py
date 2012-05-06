from abjad.tools.timeintervaltools import *


def test_TimeIntervalTreeDictionary__get_tools_package_qualified_repr_pieces_01():

    a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
    b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
    c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
    d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])

    treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
    
    pieces = treedict._get_tools_package_qualified_repr_pieces()

    assert pieces == [
        'timeintervaltools.TimeIntervalTreeDictionary({',
        "\t'a': timeintervaltools.TimeIntervalTree([",
        '\t\ttimeintervaltools.TimeInterval(',
        '\t\t\tOffset(0, 1),',
        '\t\t\tOffset(1, 1),',
        '\t\t\t{',
        "\t\t\t\t'name': 'a',",
        '\t\t\t}),',
        '\t\t]),',
        "\t'c': timeintervaltools.TimeIntervalTree([",
        '\t\ttimeintervaltools.TimeInterval(',
        '\t\t\tOffset(0, 1),',
        '\t\t\tOffset(3, 1),',
        '\t\t\t{',
        "\t\t\t\t'name': 'c',",
        '\t\t\t}),',
        '\t\t]),',
        "\t'b': timeintervaltools.TimeIntervalTree([",
        '\t\ttimeintervaltools.TimeInterval(',
        '\t\t\tOffset(1, 1),',
        '\t\t\tOffset(2, 1),',
        '\t\t\t{',
        "\t\t\t\t'name': 'b',",
        '\t\t\t}),',
        '\t\t]),',
        "\t'd': timeintervaltools.TimeIntervalTree([",
        '\t\ttimeintervaltools.TimeInterval(',
        '\t\t\tOffset(2, 1),',
        '\t\t\tOffset(3, 1),',
        '\t\t\t{',
        "\t\t\t\t'name': 'd',",
        '\t\t\t}),',
        '\t\t]),',
        '\t})'
    ]
