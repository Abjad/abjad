from abjad import *


def test_lilytools_MidiBlock_01( ):

   midi_block = lilytools.MidiBlock( )

   r'''
   \midi { }
   '''

   assert midi_block.format == '\\midi { }'
