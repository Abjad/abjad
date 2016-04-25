# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_PitchedQEvent___init___01():

    q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])

    assert q_event.offset == durationtools.Offset(130)
    assert q_event.pitches == (
        NamedPitch(0),
        NamedPitch(1),
        NamedPitch(4)
        )
    assert q_event.attachments == ()


def test_quantizationtools_PitchedQEvent___init___02():

    q_event = quantizationtools.PitchedQEvent(
        durationtools.Offset(133, 5),
        [NamedPitch('fss')],
        attachments = ['foo', 'bar', 'baz']
        )

    assert q_event.offset == durationtools.Offset(133, 5)
    assert q_event.pitches == (NamedPitch('fss'),)
    assert q_event.attachments == ('foo', 'bar', 'baz')
