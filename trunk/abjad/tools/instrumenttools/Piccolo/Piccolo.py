from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class Piccolo(Flute):
   '''.. versionadded:: 1.1.2

   Abjad model of the piccolo.
   '''

   def __init__(self):
      Flute.__init__(self)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c''")
