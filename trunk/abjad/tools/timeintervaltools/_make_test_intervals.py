def _make_test_intervals():
    from abjad.tools import timeintervaltools

    return [
        timeintervaltools.TimeInterval(0, 3,   {'name': 'a'}),
        timeintervaltools.TimeInterval(5, 13,  {'name': 'b'}),
        timeintervaltools.TimeInterval(6, 10,  {'name': 'c'}),
        timeintervaltools.TimeInterval(8, 9,   {'name': 'd'}),
        timeintervaltools.TimeInterval(15, 23, {'name': 'e'}),
        timeintervaltools.TimeInterval(16, 21, {'name': 'f'}),
        timeintervaltools.TimeInterval(17, 19, {'name': 'g'}),
        timeintervaltools.TimeInterval(19, 20, {'name': 'h'}),
        timeintervaltools.TimeInterval(25, 30, {'name': 'i'}),
        timeintervaltools.TimeInterval(26, 29, {'name': 'j'}),
        timeintervaltools.TimeInterval(32, 34, {'name': 'k'}),
        timeintervaltools.TimeInterval(34, 37, {'name': 'l'}),
    ]
