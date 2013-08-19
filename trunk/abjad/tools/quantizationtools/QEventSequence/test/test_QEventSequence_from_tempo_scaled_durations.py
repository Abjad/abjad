# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import quantizationtools


def test_QEventSequence_from_tempo_scaled_durations_01():
    r'''Test basic functionality.
    '''

    durations = [durationtools.Duration(x) for x in 
        [(1, 4), (1, 3), (1, 7), (2, 5), (3, 4)]]
    tempo = contexttools.TempoMark((1, 4), 55)
    q_events = quantizationtools.QEventSequence.from_tempo_scaled_durations(
        durations, tempo)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(12000, 11),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(28000, 11),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(244000, 77),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(34400, 7),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(630400, 77)
            )
    ))


def test_QEventSequence_from_tempo_scaled_durations_02():
    r'''Silences are fused.
    '''

    durations = [durationtools.Duration(x) for x in
        [(1, 4), (-1, 4), (1, 4), (1, 4), (-1, 4), (-1, 4), (1, 4)]]
    tempo = contexttools.TempoMark((1, 4), 77)
    q_events = quantizationtools.QEventSequence.from_tempo_scaled_durations(
        durations, tempo)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(60000, 77)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(120000, 77),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(180000, 77),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(240000, 77)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(360000, 77),
            (pitchtools.NamedPitch("c'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(60000, 11)
            )
    ))
