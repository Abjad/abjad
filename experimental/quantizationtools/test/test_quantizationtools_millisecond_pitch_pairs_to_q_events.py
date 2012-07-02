from abjad.tools import durationtools
from abjad.tools import pitchtools
from experimental import quantizationtools


def test_quantizationtools_millisecond_pitch_pairs_to_q_events_01():

    durations = [100, 200, 100, 300, 350, 400, 600]
    pitches = [0, None, None, [1, 4], None, 5, 7]
    pairs = zip(durations, pitches)

    q_events = quantizationtools.millisecond_pitch_pairs_to_q_events(pairs)

    assert q_events == [
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0),
            (pitchtools.NamedChromaticPitch("c'"),)
            ),
        quantizationtools.UnpitchedQEvent(
            durationtools.Offset(100, 1)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(400, 1),
            (
                pitchtools.NamedChromaticPitch("cs'"),
                pitchtools.NamedChromaticPitch("e'")
            )
            ),
        quantizationtools.UnpitchedQEvent(
            durationtools.Offset(700, 1)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1050, 1),
            (pitchtools.NamedChromaticPitch("f'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1450, 1),
            (pitchtools.NamedChromaticPitch("g'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(2050, 1),
            )
    ]
