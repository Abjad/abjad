# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools


class Test(unittest.TestCase):

    def test_01(self):
        message = miditools.PitchBendMessage(23)
        assert message is not None
        assert message.channel_number == 0
        assert message.pitch_bend == 23

    def test_02(self):
        data = b'\x00\xE0\x41\x5a\x83\x00\xE0\x7F\x7F'
        index = 1
        message, index = miditools.PitchBendMessage._from_bytes(data, index=index)
        assert type(message) is miditools.PitchBendMessage
        assert message.channel_number == 0
        assert message.pitch_bend == 11585
        assert index == 4

    def test_03(self):
        data = b'\x00\xE0\x41\x5a\x83\x00\xE1\x7F\x7F'
        index = 6
        message, index = miditools.PitchBendMessage._from_bytes(data, index=index)
        assert type(message) is miditools.PitchBendMessage
        assert message.channel_number == 1
        assert message.pitch_bend == 16383
        assert index == 9
