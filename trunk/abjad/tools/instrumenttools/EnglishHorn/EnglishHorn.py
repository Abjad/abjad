from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._DoubleReedInstrument import _DoubleReedInstrument


class EnglishHorn(_DoubleReedInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the English horn.
   '''

   def __init__(self):
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch('f')
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self._copy_primary_clefs_to_all_clefs( )
