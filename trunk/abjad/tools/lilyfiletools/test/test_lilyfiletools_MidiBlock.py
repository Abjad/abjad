from abjad import *


def test_lilyfiletools_MidiBlock_01( ):

   midi_block = lilyfiletools.MidiBlock( )

   r'''
   \midi { }
   '''

   assert midi_block.format == '\\midi { }'
