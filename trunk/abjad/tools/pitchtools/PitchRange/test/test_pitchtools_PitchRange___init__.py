from abjad import *


def test_pitchtools_PitchRange___init___01( ):
    '''Init infinite pitch range.'''

    pr = pitchtools.PitchRange( )
    assert pr._start is None
    assert pr._stop is None


def test_pitchtools_PitchRange___init___02( ):
    '''Init stop-specified pitch range.'''

    pr = pitchtools.PitchRange((-39, 'inclusive'), None)
    assert pr._start == (pitchtools.NamedChromaticPitch(-39), 'inclusive')
    assert pr._stop is None

    pr = pitchtools.PitchRange((-39, 'exclusive'), None)
    assert pr._start == (pitchtools.NamedChromaticPitch(-39), 'exclusive')
    assert pr._stop is None


def test_pitchtools_PitchRange___init___03( ):
    '''Init start-specified pitch range.'''

    pr = pitchtools.PitchRange(None, (48, 'inclusive'))
    assert pr._start is None
    assert pr._stop == (pitchtools.NamedChromaticPitch(48), 'inclusive')

    pr = pitchtools.PitchRange(None, (48, 'exclusive'))
    assert pr._start is None
    assert pr._stop == (pitchtools.NamedChromaticPitch(48), 'exclusive')


def test_pitchtools_PitchRange___init___04( ):
    '''Init start- and stop-specified pitch range.'''

    pr = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
    assert pr._start == (pitchtools.NamedChromaticPitch(-39), 'inclusive')
    assert pr._stop == (pitchtools.NamedChromaticPitch(48), 'inclusive')


def test_pitchtools_PitchRange___init___05( ):
    '''Short-form init with only integers.'''

    pr = pitchtools.PitchRange(-39, 48)
    assert pr._start == (pitchtools.NamedChromaticPitch(-39), 'inclusive')
    assert pr._stop == (pitchtools.NamedChromaticPitch(48), 'inclusive')


def test_pitchtools_PitchRange___init___06( ):
    '''Init pitch range from other pitch range.
    '''

    pitch_range_1 = pitchtools.PitchRange(-39, 48)
    pitch_range_2 = pitchtools.PitchRange(pitch_range_1)

    assert isinstance(pitch_range_1, pitchtools.PitchRange)
    assert isinstance(pitch_range_2, pitchtools.PitchRange)
    assert pitch_range_1 == pitch_range_2
    assert pitch_range_1 is not pitch_range_2


def test_pitchtools_PitchRange___init___07( ):
    '''Init pitch range from pair.
    '''

    pitch_range_1 = pitchtools.PitchRange(-39, 48)
    pitch_range_2 = pitchtools.PitchRange((-39, 48))

    assert pitch_range_1 == pitch_range_2

