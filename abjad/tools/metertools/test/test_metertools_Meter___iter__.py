# -*- coding: utf-8 -*-
from abjad import *


def test_metertools_Meter___iter___01():

    bh = metertools.Meter(TimeSignature((3, 8)))

    result = [x for x in bh]

    assert result == [
        (durationtools.Offset(0, 1), durationtools.Offset(1, 8)),
        (durationtools.Offset(1, 8), durationtools.Offset(1, 4)),
        (durationtools.Offset(1, 4), durationtools.Offset(3, 8)),
        (durationtools.Offset(0, 1), durationtools.Offset(3, 8))
    ]
