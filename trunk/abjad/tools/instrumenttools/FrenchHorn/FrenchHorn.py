from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument
from abjad.tools.instrumenttools._WindInstrument import _WindInstrument


class FrenchHorn(_BrassInstrument, _WindInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the French horn.
   '''

   def __init__(self):
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('f')
      self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
