# -*- encoding: utf-8 -*-
from abjad import *


def test_quantizationtools_QEventSequence_from_millisecond_pitch_pairs_01():

    durations = [100, 200, 100, 300, 350, 400, 600]
    pitches = [0, None, None, [1, 4], None, 5, 7]
    pairs = zip(durations, pitches)

    q_events = quantizationtools.QEventSequence.from_millisecond_pitch_pairs(
        pairs)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(100, 1)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(400, 1),
            (
                pitchtools.NamedPitch("cs'"),
                pitchtools.NamedPitch("e'")
            )
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(700, 1)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1050, 1),
            (pitchtools.NamedPitch("f'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1450, 1),
            (pitchtools.NamedPitch("g'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(2050, 1),
            )
    ))
