# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools


class Test(unittest.TestCase):

    def test_01(self):
        message = miditools.ControllerMessage(23, 65)
        assert message is not None
        assert message.channel_number == 0
        assert message.controller_number == 23
        assert message.controller_value == 65

    def test_02(self):
        data = b'\x00\xB0\x41\x5a\x83\x00\xB0\x41\x00'
        index = 1
        message, index = miditools.ControllerMessage._from_bytes(data, index=index)
        assert type(message) is miditools.ControllerMessage
        assert message.channel_number == 0
        assert message.controller_number == 65
        assert message.controller_value == 90
        assert index == 4

    def test_03(self):
        data = b'\x00\xB0\x41\x5a\x83\x00\xB1\x41\x00'
        index = 6
        message, index = miditools.ControllerMessage._from_bytes(data, index=index)
        assert type(message) is miditools.ControllerMessage
        assert message.channel_number == 1
        assert message.controller_number == 65
        assert message.controller_value == 0
        assert index == 9
