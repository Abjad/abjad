from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._WindInstrument import _WindInstrument


class Flute(_WindInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the flute.
   '''

   def __init__(self, 
      instrument_name = 'Flute', short_instrument_name = 'Fl.', target_context = None):
      _WindInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self._copy_primary_clefs_to_all_clefs( )
