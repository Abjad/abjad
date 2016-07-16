# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools


class Test(unittest.TestCase):

    def test_01(self):
        message = miditools.NoteOffMessage(23, 65)
        assert message is not None
        assert message.channel_number == 0
        assert message.pitch == 23
        assert message.velocity == 65

    def test_02(self):
        data = b'\x00\x80\x41\x5a\x83\x00\x80\x41\x00'
        index = 1
        message, index = miditools.NoteOffMessage._from_bytes(data, index=index)
        assert type(message) is miditools.NoteOffMessage
        assert message.channel_number == 0
        assert message.pitch == 65
        assert message.velocity == 90
        assert index == 4

    def test_03(self):
        data = b'\x00\x80\x41\x5a\x83\x00\x81\x41\x00'
        index = 6
        message, index = miditools.NoteOffMessage._from_bytes(data, index=index)
        assert type(message) is miditools.NoteOffMessage
        assert message.channel_number == 1
        assert message.pitch == 65
        assert message.velocity == 0
        assert index == 9
