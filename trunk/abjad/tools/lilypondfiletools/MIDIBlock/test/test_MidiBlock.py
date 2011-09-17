from abjad import *


def test_MIDIBlock_01():

    MIDI_block = lilypondfiletools.MIDIBlock()

    r'''
    \MIDI {}
    '''

    assert MIDI_block.format == '\\MIDI {}'
