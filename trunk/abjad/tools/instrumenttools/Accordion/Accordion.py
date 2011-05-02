from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._KeyboardInstrument import _KeyboardInstrument
from abjad.tools.instrumenttools._ReedInstrument import _ReedInstrument


class Accordion(_KeyboardInstrument, _ReedInstrument):
   '''.. versionadded 1.1.2

   Abjad model of the accordion.
   '''

   def __init__(self):
      _KeyboardInstrument.__init__(self)
      self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
