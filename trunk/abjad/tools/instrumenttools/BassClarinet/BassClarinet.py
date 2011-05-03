from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Clarinet import Clarinet


class BassClarinet(Clarinet):
   '''.. versionadded:: 1.1.2

   Abjad model of the bass clarinet.
   '''

   def __init__(self):
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch('bf')
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self.all_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
