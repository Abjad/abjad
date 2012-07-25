from abjad.tools import durationtools
from experimental import quantizationtools


def test_TerminalQEvent___init___01():

    q_event = quantizationtools.TerminalQEvent(154)

    assert q_event.offset == durationtools.Offset(154)
