from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._SingleReedInstrument import _SingleReedInstrument


class EFlatClarinet(_SingleReedInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the E-flat clarinet.
   '''

   def __init__(self):
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("ef'")
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self._copy_primary_clefs_to_all_clefs( )
