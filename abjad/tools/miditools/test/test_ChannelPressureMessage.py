# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools


class Test(unittest.TestCase):

    def test_01(self):
        message = miditools.ChannelPressureMessage(127)
        assert message is not None
        assert message.channel_number == 0
        assert message.velocity == 127

    def test_02(self):
        data = b'\x00\xd0\x5a\x83\x00\xd1\x5c'
        index = 1
        message, index = miditools.ChannelPressureMessage._from_bytes(data, index=index)
        assert type(message) is miditools.ChannelPressureMessage
        assert message.channel_number == 0
        assert message.velocity == 90

    def test_03(self):
        data = b'\x00\xd0\x5a\x83\x00\xd1\x5c'
        index = 5
        message, index = miditools.ChannelPressureMessage._from_bytes(data, index=index)
        assert type(message) is miditools.ChannelPressureMessage
        assert message.channel_number == 1
        assert message.velocity == 92
