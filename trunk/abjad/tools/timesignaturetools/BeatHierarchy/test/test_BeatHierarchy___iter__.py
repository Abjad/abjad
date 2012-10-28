from abjad import *
#from experimental import *
import py
py.test.skip('back-dependency to experimental is not allowed.')


def test_BeatHierarchy___iter___01():

    bh = timesignaturetools.BeatHierarchy(contexttools.TimeSignatureMark((3, 8)))

    result = [x for x in bh]

    assert result == [
        (durationtools.Offset(0, 1), durationtools.Offset(1, 8)),
        (durationtools.Offset(1, 8), durationtools.Offset(1, 4)),
        (durationtools.Offset(1, 4), durationtools.Offset(3, 8)),
        (durationtools.Offset(0, 1), durationtools.Offset(3, 8))
    ]
