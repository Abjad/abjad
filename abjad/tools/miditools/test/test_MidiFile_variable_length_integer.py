# -*- encoding: utf-8 -*-
from abjad.tools import miditools
import unittest


class Test(unittest.TestCase):

    def test_01(self):
        data = b'\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00000000
        assert index == 1
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_02(self):
        data = b'\x40'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00000040
        assert index == 1
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_03(self):
        data = b'\x7F'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x0000007F
        assert index == 1
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_04(self):
        data = b'\x81\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00000080
        assert index == 2
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_05(self):
        data = b'\xC0\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00002000
        assert index == 2
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_06(self):
        data = b'\xFF\x7F'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00003FFF
        assert index == 2
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_07(self):
        data = b'\x81\x80\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00004000
        assert index == 3
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_08(self):
        data = b'\xC0\x80\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00100000
        assert index == 3
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_09(self):
        data = b'\xFF\xFF\x7F'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x001FFFFF
        assert index == 3
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_10(self):
        data = b'\x81\x80\x80\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x00200000
        assert index == 4
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_11(self):
        data = b'\xC0\x80\x80\x00'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x08000000
        assert index == 4
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data

    def test_12(self):
        data = b'\xFF\xFF\xFF\x7F'
        value, index = miditools.MidiFile._variable_length_integer_from_bytes(data)
        assert value == 0x0FFFFFFF
        assert index == 4
        result = miditools.MidiFile._bytes_from_variable_length_integer(value)
        assert result == data
