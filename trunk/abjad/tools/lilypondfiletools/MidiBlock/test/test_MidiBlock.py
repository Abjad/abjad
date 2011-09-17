from abjad import *


def test_MidiBlock_01():

    midi_block = lilypondfiletools.MidiBlock()

    r'''
    \midi {}
    '''

    assert midi_block.format == '\\midi {}'
