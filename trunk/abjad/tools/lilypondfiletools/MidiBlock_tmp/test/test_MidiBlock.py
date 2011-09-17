from abjad import *


def test_MidiBlock_tmp_01():

    midi_block = lilypondfiletools.MidiBlock_tmp()

    r'''
    \midi {}
    '''

    assert midi_block.format == '\\midi {}'
