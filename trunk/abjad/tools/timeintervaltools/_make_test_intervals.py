from abjad.tools.timeintervaltools import TimeInterval


def _make_test_intervals():

    return [
        TimeInterval(0, 3,   {'name': 'a'}),
        TimeInterval(5, 13,  {'name': 'b'}),
        TimeInterval(6, 10,  {'name': 'c'}),
        TimeInterval(8, 9,   {'name': 'd'}),
        TimeInterval(15, 23, {'name': 'e'}),
        TimeInterval(16, 21, {'name': 'f'}),
        TimeInterval(17, 19, {'name': 'g'}),
        TimeInterval(19, 20, {'name': 'h'}),
        TimeInterval(25, 30, {'name': 'i'}),
        TimeInterval(26, 29, {'name': 'j'}),
        TimeInterval(32, 34, {'name': 'k'}),
        TimeInterval(34, 37, {'name': 'l'}),
    ]
