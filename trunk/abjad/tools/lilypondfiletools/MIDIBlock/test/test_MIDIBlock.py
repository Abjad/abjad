from abjad import *


def test_MIDIBlock_01():

    MIDI_block = lilypondfiletools.MIDIBlock()

    r'''
    \midi {}
    '''

    assert MIDI_block.lilypond_format == '\\midi {}'
