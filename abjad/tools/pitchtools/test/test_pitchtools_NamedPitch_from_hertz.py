from abjad import NamedPitch


def test_pitchtools_NamedPitch_from_hertz_01():
    for i in range(1, 1001):
        NamedPitch.from_hertz(i)
