from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Cello(_StringInstrument):
   '''.. versionadded:: 1.1.2

   Abjad model of the cello.
   '''

   def __init__(self):
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('bass')]
      self.all_clefs = [
         contexttools.ClefMark('bass'), 
         contexttools.ClefMark('tenor'), 
         contexttools.ClefMark('treble')]
