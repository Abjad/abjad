# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools


class Test(unittest.TestCase):

    def test_01(self):
        message = miditools.TextMessage('Hello world!')
        assert message is not None
        assert message.text == 'Hello world!'

    def test_02(self):
        data = b'\xff\x01\x09\x63\x72\x65\x61\x74\x6f\x72\x3a\x20\x00'
        index = 1
        message, index = miditools.TextMessage._from_bytes(data, index)
        assert type(message) == miditools.TextMessage
        assert message.text == 'creator: '
        assert index == 12
