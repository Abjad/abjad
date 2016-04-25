# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval_to_named_interval_01():

    numbered_interval = pitchtools.NumberedInterval(0)
    named_interval = numbered_interval.to_named_interval(1)
    assert named_interval == pitchtools.NamedInterval('perfect', 1)

    numbered_interval = pitchtools.NumberedInterval(1)
    named_interval = numbered_interval.to_named_interval(1)
    assert named_interval == pitchtools.NamedInterval('augmented', 1)

    numbered_interval = pitchtools.NumberedInterval(0)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('diminished', 2)

    numbered_interval = pitchtools.NumberedInterval(1)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('minor', 2)

    numbered_interval = pitchtools.NumberedInterval(2)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('major', 2)

    numbered_interval = pitchtools.NumberedInterval(3)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('augmented', 2)


def test_pitchtools_NumberedInterval_to_named_interval_02():

    numbered_interval = pitchtools.NumberedInterval(0)
    named_interval = numbered_interval.to_named_interval(1)
    assert named_interval == pitchtools.NamedInterval('perfect', 1)

    numbered_interval = pitchtools.NumberedInterval(-1)
    named_interval = numbered_interval.to_named_interval(1)
    assert named_interval == pitchtools.NamedInterval('augmented', -1)

    numbered_interval = pitchtools.NumberedInterval(0)
    named_interval = numbered_interval.to_named_interval(2)
    # THE ASCENDING INTERVAL HERE IS WEIRD #
    assert named_interval == pitchtools.NamedInterval('diminished', 2)

    numbered_interval = pitchtools.NumberedInterval(-1)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('minor', -2)

    numbered_interval = pitchtools.NumberedInterval(-2)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('major', -2)

    numbered_interval = pitchtools.NumberedInterval(-3)
    named_interval = numbered_interval.to_named_interval(2)
    assert named_interval == pitchtools.NamedInterval('augmented', -2)
