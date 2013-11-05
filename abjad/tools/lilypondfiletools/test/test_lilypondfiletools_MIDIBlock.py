# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_MIDIBlock_01():

    MIDI_block = lilypondfiletools.MIDIBlock()

    assert testtools.compare(
        MIDI_block,
        r'''
        \midi {}
        '''
        )
