from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._KeyboardInstrument import _KeyboardInstrument


class Piano(_KeyboardInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the piano.
   '''

   def __init__(self):
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
