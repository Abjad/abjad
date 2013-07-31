from abjad import *


def test_pitchtools_calculate_melodic_counterpoint_interval_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(10)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(9)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(9)


def test_pitchtools_calculate_melodic_counterpoint_interval_02():
    r'''Ascending octave.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(8)


def test_pitchtools_calculate_melodic_counterpoint_interval_03():
    r'''Ascending intervals less than an octave.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(3)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(2)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(2)


def test_pitchtools_calculate_melodic_counterpoint_interval_04():
    r'''Unison.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(1)


def test_pitchtools_calculate_melodic_counterpoint_interval_05():
    r'''Descending intervals greater than an octave.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-10)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-9)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-9)


def test_pitchtools_calculate_melodic_counterpoint_interval_06():
    r'''Descending octave.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-8)


def test_pitchtools_calculate_melodic_counterpoint_interval_07():
    r'''Descending intervals less than an octave.
    '''

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-3)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-2)

    mcpi = pitchtools.calculate_melodic_counterpoint_interval(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-2)
