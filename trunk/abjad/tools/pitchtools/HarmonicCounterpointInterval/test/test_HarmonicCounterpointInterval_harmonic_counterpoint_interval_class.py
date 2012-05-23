from abjad import *


def test_HarmonicCounterpointInterval_harmonic_counterpoint_interval_class_01():
    '''Unison.'''

    hcpi = pitchtools.HarmonicCounterpointInterval(1)
    hcpic = hcpi.harmonic_counterpoint_interval_class
    assert hcpic == pitchtools.HarmonicCounterpointIntervalClass(1)


def test_HarmonicCounterpointInterval_harmonic_counterpoint_interval_class_02():
    '''Intervals greater than a unison and less than an octave.'''

    hcpi = pitchtools.HarmonicCounterpointInterval(2)
    hcpic = hcpi.harmonic_counterpoint_interval_class
    assert hcpic == pitchtools.HarmonicCounterpointIntervalClass(2)

    hcpi = pitchtools.HarmonicCounterpointInterval(7)
    hcpic = hcpi.harmonic_counterpoint_interval_class
    assert hcpic == pitchtools.HarmonicCounterpointIntervalClass(7)


def test_HarmonicCounterpointInterval_harmonic_counterpoint_interval_class_03():
    '''Octave.'''

    hcpi = pitchtools.HarmonicCounterpointInterval(8)
    hcpic = hcpi.harmonic_counterpoint_interval_class
    assert hcpic == pitchtools.HarmonicCounterpointIntervalClass(8)


def test_HarmonicCounterpointInterval_harmonic_counterpoint_interval_class_04():
    '''Intervals greater than an octave.'''

    hcpi = pitchtools.HarmonicCounterpointInterval(9)
    hcpic = hcpi.harmonic_counterpoint_interval_class
    assert hcpic == pitchtools.HarmonicCounterpointIntervalClass(2)

    hcpi = pitchtools.HarmonicCounterpointInterval(10)
    hcpic = hcpi.harmonic_counterpoint_interval_class
    assert hcpic == pitchtools.HarmonicCounterpointIntervalClass(3)
