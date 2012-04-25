from abjad import *
from abjad.tools import durationtools


def test_SchemeMoment_duration_01():

    scheme_moment = schemetools.SchemeMoment((1, 68))

    assert scheme_moment.duration == durationtools.Duration((1, 68))
