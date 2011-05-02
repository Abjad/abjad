from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument


class Trombone(_BrassInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the trombone.
   '''

   def __init__(self):
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
      self._copy_primary_clefs_to_all_clefs( )
