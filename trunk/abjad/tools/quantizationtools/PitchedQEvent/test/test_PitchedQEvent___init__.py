from abjad.tools import durationtools
from abjad.tools import pitchtools
from abjad.tools import quantizationtools


def test_PitchedQEvent___init___01():

    q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])

    assert q_event.offset == durationtools.Offset(130)
    assert q_event.pitches == (
        pitchtools.NamedChromaticPitch(0),
        pitchtools.NamedChromaticPitch(1),
        pitchtools.NamedChromaticPitch(4)
        )
    assert q_event.attachments == ()


def test_PitchedQEvent___init___02():

    q_event = quantizationtools.PitchedQEvent(
        durationtools.Offset(133, 5),
        [pitchtools.NamedChromaticPitch('fss')],
        attachments = ['foo', 'bar', 'baz']
        )

    assert q_event.offset == durationtools.Offset(133, 5)
    assert q_event.pitches == (pitchtools.NamedChromaticPitch('fss'),)
    assert q_event.attachments == ('foo', 'bar', 'baz')

