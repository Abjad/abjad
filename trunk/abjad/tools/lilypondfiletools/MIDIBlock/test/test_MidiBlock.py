from abjad import *


def test_MIDIBlock_01():

    midi_block = lilypondfiletools.MIDIBlock()

    r'''
    \midi {}
    '''

    assert midi_block.format == '\\midi {}'
