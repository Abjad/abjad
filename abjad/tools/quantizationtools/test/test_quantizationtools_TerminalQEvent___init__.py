import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_TerminalQEvent___init___01():

    q_event = quantizationtools.TerminalQEvent(154)

    assert q_event.offset == abjad.Offset(154)
