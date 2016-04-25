# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QEventSequence_from_millisecond_durations_01():
    r'''Test basic functionality.
    '''

    durations = mathtools.difference_series(
        [x[0] for x in quantizationtools.make_test_time_segments()])
    q_events = quantizationtools.QEventSequence.from_millisecond_durations(
        durations)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(163, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(511, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(627, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1208, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1417, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1997, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(3204, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(3297, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(4087, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(4296, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(4830, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(6362, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(6595, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(6687, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(7013, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(7245, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(7872, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(8197, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(8359, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(8638, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(8731, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(8917, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(9288, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(9404, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(10240, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(10356, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(10496, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(10890, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(11169, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(11285, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(11424, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(12307, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(12957, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(13073, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(13653, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(13979, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(14234, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(15256, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(15883, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(16022, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(16649, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(16927, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(17044, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(17276, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(18483, 1)
            )
    ))


def test_quantizationtools_QEventSequence_from_millisecond_durations_02():
    r'''Silences are not fused.
    '''

    durations = [100, -100, 100, -100, -100, 100]
    q_events = quantizationtools.QEventSequence.from_millisecond_durations(
        durations, fuse_silences=False)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0),
            (NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(100)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(200),
            (NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(300)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(400)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(500),
            (NamedPitch("c'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(600)
            )
    ))


def test_quantizationtools_QEventSequence_from_millisecond_durations_03():
    r'''Silences are fused.
    '''

    durations = [100, -100, 100, -100, -100, 100]
    q_events = quantizationtools.QEventSequence.from_millisecond_durations(
        durations, fuse_silences=True)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0),
            (NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(100)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(200),
            (NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(300)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(500),
            (NamedPitch("c'"),)
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(600)
            )
    ))
