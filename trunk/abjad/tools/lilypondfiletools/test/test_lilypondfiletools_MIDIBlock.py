# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_MIDIBlock_01():

    MIDI_block = lilypondfiletools.MIDIBlock()

    r'''
    \midi {}
    '''

    assert MIDI_block.lilypond_format == '\\midi {}'
