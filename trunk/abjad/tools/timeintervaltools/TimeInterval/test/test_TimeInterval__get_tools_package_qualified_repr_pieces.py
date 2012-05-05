from abjad.tools.durationtools import Offset
from abjad.tools import timeintervaltools


def test_TimeInterval__get_tools_package_qualified_repr_pieces_01():

    t = timeintervaltools.TimeInterval(0, 1, {
        'a': timeintervaltools.TimeInterval(3, 4, {'x': 'y'}), 'b': 3
    })

    assert t._get_tools_package_qualified_repr_pieces() == [
        'timeintervaltools.TimeInterval(',
        '\tOffset(0, 1),',
        '\tOffset(1, 1),',
        '\t{',
        "\t\t'a': timeintervaltools.TimeInterval(",
        '\t\t\tOffset(3, 1),',
        '\t\t\tOffset(4, 1),',
        '\t\t\t{',
        "\t\t\t\t'x': 'y',",
        '\t\t\t}),',
        "\t\t'b': 3,",
        '\t})'
    ]
