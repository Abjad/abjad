# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools


class Test(unittest.TestCase):

    def test_01(self):
        message = miditools.ProgramChangeMessage(23)
        assert message is not None
        assert message.channel_number == 0
        assert message.program_number == 23

    def test_02(self):
        data = b'\x00\xC0\x07\x83\x00\xC1\x17'
        index = 1
        message, index = miditools.ProgramChangeMessage._from_bytes(data, index=index)
        assert type(message) is miditools.ProgramChangeMessage
        assert message.channel_number == 0
        assert message.program_number == 7

    def test_03(self):
        data = b'\x00\xC0\x07\x83\x00\xC1\x17'
        index = 5
        message, index = miditools.ProgramChangeMessage._from_bytes(data, index=index)
        assert type(message) is miditools.ProgramChangeMessage
        assert message.channel_number == 1
        assert message.program_number == 23
