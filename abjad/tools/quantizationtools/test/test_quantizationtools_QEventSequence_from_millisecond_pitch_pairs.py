import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_QEventSequence_from_millisecond_pitch_pairs_01():

    durations = [100, 200, 100, 300, 350, 400, 600]
    pitches = [0, None, None, [1, 4], None, 5, 7]
    pairs = tuple(zip(durations, pitches))

    q_events = quantizationtools.QEventSequence.from_millisecond_pitch_pairs(
        pairs)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            abjad.Offset(0),
            (abjad.NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            abjad.Offset(100, 1)
            ),
        quantizationtools.PitchedQEvent(
            abjad.Offset(400, 1),
            (
                abjad.NamedPitch("cs'"),
                abjad.NamedPitch("e'")
            )
            ),
        quantizationtools.SilentQEvent(
            abjad.Offset(700, 1)
            ),
        quantizationtools.PitchedQEvent(
            abjad.Offset(1050, 1),
            (abjad.NamedPitch("f'"),)
            ),
        quantizationtools.PitchedQEvent(
            abjad.Offset(1450, 1),
            (abjad.NamedPitch("g'"),)
            ),
        quantizationtools.TerminalQEvent(
            abjad.Offset(2050, 1),
            )
    ))
