from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import TimeInterval, TimeIntervalTree


def test_TimeIntervalTree__get_tools_package_qualified_repr_pieces_01():

    a = TimeInterval(Offset(-1, 1), Offset(3, 1), {
        'a': 1, 'b': 2, 't': TimeInterval(Offset(2, 1), Offset(3, 1), {'x': 'b'})})
    b = TimeInterval(Offset(0, 1), Offset(1, 1), {'x': 'y'})
    tree = TimeIntervalTree([a, b])

    assert tree._get_tools_package_qualified_repr_pieces() == [
        'timeintervaltools.TimeIntervalTree([',
        '\ttimeintervaltools.TimeInterval(',
        '\t\tOffset(-1, 1),',
        '\t\tOffset(3, 1),',
        '\t\t{',
        "\t\t\t'a': 1,",
        "\t\t\t'b': 2,",
        "\t\t\t't': timeintervaltools.TimeInterval(",
        '\t\t\t\tOffset(2, 1),',
        '\t\t\t\tOffset(3, 1),',
        '\t\t\t\t{',
        "\t\t\t\t\t'x': 'b',",
        '\t\t\t\t}),',
        '\t\t}),',
        '\ttimeintervaltools.TimeInterval(',
        '\t\tOffset(0, 1),',
        '\t\tOffset(1, 1),',
        '\t\t{',
        "\t\t\t'x': 'y',",
        '\t\t}),',
        '\t])'
    ]
